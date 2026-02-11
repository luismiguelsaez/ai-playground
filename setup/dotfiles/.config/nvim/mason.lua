return {
  "mason-org/mason-lspconfig.nvim",
  opts = {
    ensure_installed = { "lua_ls", "pyright", "ruff" },
  },
  dependencies = {
    { "mason-org/mason.nvim", opts = {} },
    "neovim/nvim-lspconfig",
  },
  config = function()
    vim.lsp.config("pyright", {
      settings = {
        python = {
          analysis = {
            useLibraryCodeForTypes = true,
            diagnosticSeverityOverrides = {
              reportUnusedVariable = "warning",
            },
            typeCheckingMode = "basic", -- Set type-checking mode to basic
            diagnosticMode = "workspace", -- Keep diagnostics but limit scope
            stubPath = "typings",
            exclude = {
              "**/venv/**",
              "**/.venv/**",
              "**/__pycache__/**",
            },
          },
        },
      },
    })
    local on_attach_ruff = function(client, _)
      if client.name == "ruff" then
        -- disable hover in favor of pyright
        client.server_capabilities.hoverProvider = false
      end
    end
    vim.lsp.config("ruff", {
      on_attach = on_attach_ruff,
      init_options = {
        settings = {
          args = {
            "--ignore",
            "F821",
            "--ignore",
            "E402",
            "--ignore",
            "E722",
            "--ignore",
            "E712",
          },
        },
      },
    })
    vim.lsp.handlers["textDocument/hover"] = vim.lsp.with(vim.lsp.handlers.hover, {
      border = "rounded",
      width = 70,
      height = 15,
    })
    vim.lsp.handlers["textDocument/signatureHelp"] =
      vim.lsp.with(vim.lsp.handlers.signature_help, { border = "rounded" })

    vim.keymap.set("n", "K", vim.lsp.buf.hover, {})
    vim.keymap.set("n", "<leader>gd", vim.lsp.buf.definition, {})
    vim.keymap.set("n", "<leader>gr", vim.lsp.buf.references, {})
    vim.keymap.set("n", "<leader>ca", vim.lsp.buf.code_action, {})
    vim.lsp.enable("pyright")
    vim.lsp.enable("ruff")
  end,
}
