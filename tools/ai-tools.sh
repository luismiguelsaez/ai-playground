#!/bin/bash

set -e

BASE_TOOLS_PATH=$HOME/ai/tools
BASE_MODELS_PATH=$HOME/comfy/ComfyUI/models
BASE_PID_PATH=/tmp

SWARM_ADDRESS=0.0.0.0
SWARM_PORT=8899
COMFY_ADDRESS=0.0.0.0
COMFY_PORT=8888
FORGE_ADDRESS=0.0.0.0
FORGE_PORT=8877
VLLM_ADDRESS=0.0.0.0
VLLM_PORT=8000
OPENWEBUI_ADDRESS=0.0.0.0
OPENWEBUI_PORT=3000

mkdir -p $BASE_TOOLS_PATH

case $1 in 
  "vllm")
	VLLM_PYTHON="python3.11"
	VLLM_GPUS=1
	VLLM_BASE_PATH=$BASE_TOOLS_PATH/vllm
	VLLM_PID_FILE=$BASE_PID_PATH/ai-tools-vllm.pid
	OPENWEBUI_PID_FILE=$BASE_PID_PATH/ai-tools-vllm.pid

	case $2 in
	   	"install") 
		sudo apt-get install $VLLM_PYTHON-dev
		$VLLM_PYTHON -m venv $VLLM_BASE_PATH/venv
		source $VLLM_BASE_PATH/venv/bin/activate
		pip install vllm open-webui
		;;

		"start")
		## Launch
		echo "Starting vLLM service"
		source $VLLM_BASE_PATH/venv/bin/activate

		checkpoint="Qwen/Qwen2.5-14B-Instruct-AWQ"
		$VLLM_BASE_PATH/venv/bin/vllm serve $checkpoint \
		  --host $VLLM_ADDRESS \
		  --port $VLLM_PORT \
		  --dtype auto \
		  --max-model-len 8192 \
		  --gpu-memory-utilization 0.90 \
		  --tensor-parallel-size $VLLM_GPUS >>/tmp/ai-tools-vllm.log 2>&1 &
		echo $! > $VLLM_PID_FILE

		export HOST=$OPENWEBUI_HOST
		export OPENAI_API_KEYS=dummy
		export OPENAI_API_BASE_URLS=http://$VLLM_ADDRESS:$VLLM_PORT/v1
		$VLLM_BASE_PATH/venv/bin/open-webui serve --port=$OPENWEBUI_PORT >>/tmp/ai-tools-openwebui.log 2>&1 &
		echo $! > $OPENWEBUI_PID_FILE
		;;

		"stop")
		## Stop
		echo "Stopping vLLM service"
		#[ -e $VLLM_PID_FILE ] && `kill -0 $( cat $VLLM_PID_FILE ) >/dev/null 2>&1` && kill -9 $( cat $VLLM_PID_FILE ) && rm $VLLM_PID_FILE
		killall -9 $VLLM_BASE_PATH/venv/bin/vllm
		killall -9 $VLLM_BASE_PATH/venv/bin/open-webui
		;;
	esac
  ;;
 
  "forge")
	FORGE_REPO=https://github.com/lllyasviel/stable-diffusion-webui-forge.git
	FORGE_PYTHON="python3.11"
	FORGE_BASE_PATH=$BASE_TOOLS_PATH/forge
	FORGE_CLONE_PATH=$FORGE_BASE_PATH/ForgeUI
	FORGE_MODELS_PATH=$FORGE_CLONE_PATH/models
	FORGE_PID_FILE=$BASE_PID_PATH/ai-tools-forge.pid

	case $2 in
	   	"install") 
		mkdir -p $FORGE_BASE_PATH

		if [ ! -d $FORGE_CLONE_PATH ]
		then
			git clone $FORGE_REPO $FORGE_CLONE_PATH
		fi

		sudo apt install cmake

		$FORGE_PYTHON -m venv $FORGE_BASE_PATH/venv
		source $FORGE_BASE_PATH/venv/bin/activate
		pip install --upgrade pip setuptools wheel
		#pip install joblib
		pip install -r $FORGE_CLONE_PATH/requirements_versions.txt
		pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

		sed -i 's/^#python_cmd=".*"/python_cmd="'$FORGE_PYTHON'"/g' $FORGE_CLONE_PATH/webui-user.sh

		## Link to models folders
		rm -rf $FORGE_MODELS_PATH/Stable-diffusion
		ln -nsf $BASE_MODELS_PATH/checkpoints $FORGE_MODELS_PATH/Stable-diffusion
		rm -rf $FORGE_MODELS_PATH/Lora
		ln -nsf $BASE_MODELS_PATH/loras $FORGE_MODELS_PATH/Lora
		rm -rf $FORGE_MODELS_PATH/VAE
		ln -nsf $BASE_MODELS_PATH/vae $FORGE_MODELS_PATH/VAE
		rm -rf $FORGE_CLONE_PATH/embeddings
		ln -nsf $BASE_MODELS_PATH/embeddings $FORGE_CLONE_PATH/embeddings
		;;

		"start")
		## Launch
		echo "Starting forge service"
		source $FORGE_BASE_PATH/venv/bin/activate

		#[ -e $FORGE_PID_FILE ] && `kill -0 $( cat $FORGE_PID_FILE ) >/dev/null 2>&1` && kill -9 $( cat $FORGE_PID_FILE )
		##$FORGE_BASE_PATH/venv/bin/python $FORGE_CLONE_PATH/main.py --listen $FORGE_ADDRESS --port $FORGE_PORT >>/tmp/ai-tools-forge.log 2>&1 &
		#$FORGE_BASE_PATH/venv/bin/python $FORGE_CLONE_PATH/launch.py
		#bash $FORGE_CLONE_PATH/webui.sh --listen --port $FORGE_PORT >>/tmp/ai-tools-forge.log 2>&1 &
		python -u $FORGE_CLONE_PATH/launch.py --cuda-malloc --listen --port $FORGE_PORT >>/tmp/ai-tools-forge.log 2>&1 &
		echo $! > $FORGE_PID_FILE 
		;;

		"stop")
		## Stop
		echo "Stopping forge service"
		# pkill -p $( cat $FORGE_PID_FILE )
		[ -e $FORGE_PID_FILE ] && `kill -0 $( cat $FORGE_PID_FILE ) >/dev/null 2>&1` && kill -9 $( cat $FORGE_PID_FILE ) && rm $FORGE_PID_FILE
		;;
	esac
  ;;
  "swarm")
	SWARM_REPO=https://github.com/mcmonkeyprojects/SwarmUI
	SWARM_BASE_PATH=$BASE_TOOLS_PATH/SwarmUI
	SWARM_MODELS_PATH=$SWARM_BASE_PATH/Models
	SWARM_PID_FILE=$BASE_PID_PATH/ai-tools-swarm.pid
	case $2 in
		"install")

		## Install .NET SDK
		sudo apt install -y dotnet-sdk-8.0

		## Clone repository
		if [ ! -d $SWARM_BASE_PATH/SwarmUI ]
		then
			git clone $SWARM_REPO $SWARM_BASE_PATH/SwarmUI
		fi

		## Link to models folders
		ln -nsf $BASE_MODELS_PATH/checkpoints $SWARM_MODELS_PATH/Stable-Diffusion
		ln -nsf $BASE_MODELS_PATH/loras $SWARM_MODELS_PATH/Lora
		ln -nsf $BASE_MODELS_PATH/diffusion_models $SWARM_MODELS_PATH/diffusion_models
		ln -nsf $BASE_MODELS_PATH/vae $SWARM_MODELS_PATH/VAE
		ln -nsf $BASE_MODELS_PATH/clip $SWARM_MODELS_PATH/clip
		ln -nsf $BASE_MODELS_PATH/text_encoders $SWARM_MODELS_PATH/text_encoders
		ln -nsf $BASE_MODELS_PATH/embeddings $SWARM_MODELS_PATH/Embeddings
		ln -nsf $BASE_MODELS_PATH/upscale_models $SWARM_MODELS_PATH/upscale_models
		;;
		
		"start")
		## Launch
		echo "Starting swarm service"
		[ -e $SWARM_PID_FILE ] && kill -9 $( cat $SWARM_PID_FILE )
		$BASE_TOOLS_PATH/SwarmUI/launch-linux.sh --host $SWARM_ADDRESS --port $SWARM_PORT >>/tmp/ai-tools-swarm.log 2>&1 &
		echo $! > $SWARM_PID_FILE 
		;;

		"stop")
		## Stop
		echo "Stopping swarm service"
		[ -e $SWARM_PID_FILE ] && kill -9 $( cat $SWARM_PID_FILE ) && rm $SWARM_PID_FILE
		;;
	esac
  ;;

  "comfy")
	COMFY_PYTHON="/usr/bin/python3.11"
	COMFY_REPO=https://github.com/comfyanonymous/ComfyUI
	COMFY_BASE_PATH=$BASE_TOOLS_PATH/comfy
	COMFY_CLONE_PATH=$COMFY_BASE_PATH/ComfyUI
	COMFY_NODES_PATH=$COMFY_CLONE_PATH/custom_nodes
	COMFY_MODELS_PATH=$COMFY_CLONE_PATH/models
	COMFY_PID_FILE=$BASE_PID_PATH/ai-tools-comfy.pid

	COMFY_CUSTOM_NODES=(
		ComfyUI-GGUF:https://github.com/city96/ComfyUI-GGUF
		ComfyUI-Frame-Interpolation:https://github.com/Fannovel16/ComfyUI-Frame-Interpolation
		ComfyUI-GIMM-VFI:https://github.com/kijai/ComfyUI-GIMM-VFI
		ComfyUI-KJNodes:https://github.com/kijai/ComfyUI-KJNodes
		ComfyUI-Manager:https://github.com/ltdrdata/ComfyUI-Manager
		ComfyUI_VideoEditing:https://github.com/leeguandong/ComfyUI_VideoEditing
		ComfyUI-VideoHelperSuite:https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
		ComfyUI-VideoUpscale_WithModel:https://github.com/ShmuelRonen/ComfyUI-VideoUpscale_WithModel
		ComfyUI-WanMoeKSampler:https://github.com/stduhpf/ComfyUI-WanMoeKSampler
		ComfyUI-WanVideoWrapper:https://github.com/kijai/ComfyUI-WanVideoWrapper
		rgthree-comfy:https://github.com/rgthree/rgthree-comfy
	)
	case $2 in
		"install")

		mkdir -p $COMFY_BASE_PATH

		if [ ! -d $COMFY_CLONE_PATH ]
		then
			git clone $COMFY_REPO $COMFY_CLONE_PATH
		fi

		$COMFY_PYTHON -m venv $COMFY_BASE_PATH/venv
		source $COMFY_BASE_PATH/venv/bin/activate
		pip install --upgrade pip setuptools wheel
		pip install -r $COMFY_CLONE_PATH/requirements.txt
		pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

		## Link to models folders
		rm -rf $COMFY_MODELS_PATH/checkpoints
		ln -nsf $BASE_MODELS_PATH/checkpoints $COMFY_MODELS_PATH/checkpoints
		rm -rf $COMFY_MODELS_PATH/loras
		ln -nsf $BASE_MODELS_PATH/loras $COMFY_MODELS_PATH/loras
		rm -rf $COMFY_MODELS_PATH/diffusion_models
		ln -nsf $BASE_MODELS_PATH/diffusion_models $COMFY_MODELS_PATH/diffusion_models
		rm -rf $COMFY_MODELS_PATH/vae
		ln -nsf $BASE_MODELS_PATH/vae $COMFY_MODELS_PATH/vae
		rm -rf $COMFY_MODELS_PATH/clip
		ln -nsf $BASE_MODELS_PATH/clip $COMFY_MODELS_PATH/clip
		rm -rf $COMFY_MODELS_PATH/clip_vision
		ln -nsf $BASE_MODELS_PATH/clip_vision $COMFY_MODELS_PATH/clip_vision
		rm -rf $COMFY_MODELS_PATH/text_encoders
		ln -nsf $BASE_MODELS_PATH/text_encoders $COMFY_MODELS_PATH/text_encoders
		rm -rf $COMFY_MODELS_PATH/embeddings
		ln -nsf $BASE_MODELS_PATH/embeddings $COMFY_MODELS_PATH/embeddings
		rm -rf $COMFY_MODELS_PATH/upscale_models
		ln -nsf $BASE_MODELS_PATH/upscale_models $COMFY_MODELS_PATH/upscale_models

		## Custom nodes dependencies
		pip install opencv-python diffusers gguf omegaconf cupy-cuda12x ftfy accelerate yacs timm easydict

		for custom_node in "${COMFY_CUSTOM_NODES[@]}"; do
		  key="${custom_node%%:*}"
		  value="${custom_node#*:}"
		  echo "Custom node: $key, Repository $value"
		  if [ ! -d "$COMFY_NODES_PATH/$key" ]
		  then
			echo "Cloning Custom node: $key, Repository $value"
			git clone $value $COMFY_NODES_PATH/$key
		  else
			echo "Skipping Custom node: $key, Repository $value"
		  fi
		  if [ -e "$COMFY_NODES_PATH/$key/requirements.txt" ]
		  then
			pip install -r $COMFY_NODES_PATH/$key/requirements.txt
		  else
			echo "Requirements file not found for $key"
		  fi
		done
		;;

		"start")
		## Launch
		echo "Starting comfy service"
		#[ -e $COMFY_PID_FILE ] && `kill -0 $( cat $COMFY_PID_FILE ) >/dev/null 2>&1` && kill -9 $( cat $COMFY_PID_FILE )
		$COMFY_BASE_PATH/venv/bin/python $COMFY_CLONE_PATH/main.py --listen $COMFY_ADDRESS --port $COMFY_PORT >>/tmp/ai-tools-comfy.log 2>&1 &
		echo $! > $COMFY_PID_FILE 
		;;

		"stop")
		## Stop
		echo "Stopping comfy service"
		[ -e $COMFY_PID_FILE ] && `kill -0 $( cat $COMFY_PID_FILE ) >/dev/null 2>&1` && kill -9 $( cat $COMFY_PID_FILE ) && rm $COMFY_PID_FILE
		;;
	esac
  ;;
esac
