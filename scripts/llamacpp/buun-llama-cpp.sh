#!/bin/bash

# buun-llama-cpp.sh - Compile and run llama.cpp variants
# Usage: ./buun-llama-cpp.sh <option> [options]

set -e

# Default values
REPO_URL="https://github.com/spiritbuun/buun-llama-cpp"
CLONE_PATH="/tmp"
MODEL_PATH=""
RUN_MODE="cli"
HOST="0.0.0.0"
PORT="8002"
CONTEXT_SIZE="262144"
TOKEN_CACHE="turbo3_tcq"
VALUE_CACHE="turbo2_tcq"
FLASH_ATTENTION="on"
DEVICE="CUDA0"
MAX_TOKENS="8192"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print usage information
usage() {
    echo "Usage: $0 <option> [options]"
    echo ""
    echo "Options:"
    echo "  compile    Compile llama.cpp from repository"
    echo "  run        Run llama.cpp (cli or server mode)"
    echo ""
    echo "Compile options:"
    echo "  --repo URL       Repository URL (default: $REPO_URL)"
    echo "  --path PATH      Clone path (default: $CLONE_PATH)"
    echo ""
    echo "Run options:"
    echo "  --model PATH     Path to GGUF model file (required)"
    echo "  --mode MODE      Run mode: 'cli' or 'server' (default: cli)"
    echo "  --host HOST      Server host (default: $HOST)"
    echo "  --port PORT      Server port (default: $PORT)"
    echo "  --context SIZE   Context size (default: $CONTEXT_SIZE)"
    echo "  --token-cache X  Token cache type (default: $TOKEN_CACHE)"
    echo "  --value-cache X  Value cache type (default: $VALUE_CACHE)"
    echo "  --flash-att X    Flash attention: 'on' or 'off' (default: $FLASH_ATTENTION)"
    echo "  --device X       Device (default: $DEVICE)"
    echo "  --max-tokens X   Max tokens (default: $MAX_TOKENS)"
    echo ""
    echo "Examples:"
    echo "  $0 compile"
    echo "  $0 compile --repo https://github.com/spiritbuun/buun-llama-cpp --path /tmp/buun"
    echo "  $0 run --model /path/to/model.gguf --mode server"
    echo "  $0 run --model /path/to/model.gguf --mode cli"
}

# Compile function
compile() {
    echo -e "${GREEN}=== Compiling llama.cpp ===${NC}"
    echo ""
    echo "Repository: $REPO_URL"
    echo "Clone path: $CLONE_PATH"
    echo ""
    
    # Create clone directory if it doesn't exist
    if [ ! -d "$CLONE_PATH" ]; then
        echo -e "${YELLOW}Creating directory: $CLONE_PATH${NC}"
        mkdir -p "$CLONE_PATH"
    fi
    
    # Check if repository already exists
    REPO_DIR="$CLONE_PATH/buun-llama-cpp"
    if [ -d "$REPO_DIR" ]; then
        echo -e "${YELLOW}Repository already exists at $REPO_DIR${NC}"
        echo -e "${YELLOW}Pulling latest changes...${NC}"
        cd "$REPO_DIR"
        git pull
    else
        echo -e "${YELLOW}Cloning repository...${NC}"
        git clone "$REPO_URL" "$REPO_DIR"
    fi
    
    # Build
    echo -e "${YELLOW}Building llama.cpp...${NC}"
    cd "$REPO_DIR"
    
    # Detect if CUDA is available
    if command -v nvcc &> /dev/null; then
        echo -e "${GREEN}CUDA detected, building with GPU support${NC}"
        make CUDA=1 LLAMA_FLASH_ATTN=1 LLAMA_SCALED_ROPE=1 LLAMA_K_QUANTS=1 LLAMA_MMQ=1 -j$(nproc)
    else
        echo -e "${YELLOW}CUDA not detected, building CPU version${NC}"
        make -j$(nproc)
    fi
    
    echo ""
    echo -e "${GREEN}=== Build complete ===${NC}"
    echo "Binary location: $REPO_DIR/build/bin/"
}

# Run function
run() {
    if [ -z "$MODEL_PATH" ]; then
        echo -e "${RED}Error: --model parameter is required for run option${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}=== Running llama.cpp ===${NC}"
    echo ""
    echo "Model: $MODEL_PATH"
    echo "Mode: $RUN_MODE"
    echo "Device: $DEVICE"
    echo ""
    
    # Common flags
    COMMON_FLAGS="-c $CONTEXT_SIZE -ctk $TOKEN_CACHE -ctv $VALUE_CACHE -fa $FLASH_ATTENTION --device $DEVICE -m $MODEL_PATH -n $MAX_TOKENS"
    
    # Run based on mode
    case $RUN_MODE in
        cli)
            echo -e "${YELLOW}Running llama-cli...${NC}"
            # Find the binary
            BINARY_PATH=""
            if [ -f "$CLONE_PATH/buun-llama-cpp/build/bin/llama-cli" ]; then
                BINARY_PATH="$CLONE_PATH/buun-llama-cpp/build/bin/llama-cli"
            elif command -v llama-cli &> /dev/null; then
                BINARY_PATH=$(which llama-cli)
            else
                echo -e "${RED}Error: llama-cli binary not found${NC}"
                exit 1
            fi
            
            $BINARY_PATH $COMMON_FLAGS
            ;;
        server)
            echo -e "${YELLOW}Running llama-server...${NC}"
            echo "Host: $HOST"
            echo "Port: $PORT"
            echo ""
            
            # Find the binary
            BINARY_PATH=""
            if [ -f "$CLONE_PATH/buun-llama-cpp/build/bin/llama-server" ]; then
                BINARY_PATH="$CLONE_PATH/buun-llama-cpp/build/bin/llama-server"
            elif command -v llama-server &> /dev/null; then
                BINARY_PATH=$(which llama-server)
            else
                echo -e "${RED}Error: llama-server binary not found${NC}"
                exit 1
            fi
            
            $BINARY_PATH --host $HOST --port $PORT $COMMON_FLAGS
            ;;
        *)
            echo -e "${RED}Error: Invalid mode. Use 'cli' or 'server'${NC}"
            exit 1
            ;;
    esac
}

# Parse command line arguments
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

OPTION=$1
shift

while [ $# -gt 0 ]; do
    case $1 in
        --repo)
            REPO_URL="$2"
            shift 2
            ;;
        --path)
            CLONE_PATH="$2"
            shift 2
            ;;
        --model)
            MODEL_PATH="$2"
            shift 2
            ;;
        --mode)
            RUN_MODE="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --context)
            CONTEXT_SIZE="$2"
            shift 2
            ;;
        --token-cache)
            TOKEN_CACHE="$2"
            shift 2
            ;;
        --value-cache)
            VALUE_CACHE="$2"
            shift 2
            ;;
        --flash-att)
            FLASH_ATTENTION="$2"
            shift 2
            ;;
        --device)
            DEVICE="$2"
            shift 2
            ;;
        --max-tokens)
            MAX_TOKENS="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option: $1${NC}"
            usage
            exit 1
            ;;
    esac
done

# Execute the requested option
case $OPTION in
    compile)
        compile
        ;;
    run)
        run
        ;;
    *)
        echo -e "${RED}Error: Invalid option: $OPTION${NC}"
        usage
        exit 1
        ;;
esac
