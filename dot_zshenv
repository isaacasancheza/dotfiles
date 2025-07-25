# uv
export UV_PYTHON=3.13

# pnpm
export PNPM_HOME="$HOME/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac

# auto-notify
export AUTO_NOTIFY_THRESHOLD=10

# gradle: https://github.com/gradle/gradle-completion/blob/master/README.md#additional-configuration
export GRADLE_COMPLETION_EXCLUDE_PATTERN="/(build|integTest|samples|smokeTest|testFixtures|templates|out|features)/"
export GRADLE_COMPLETION_EXCLUDE_PATTERN="gradle"

# homebrew 
export HOMEBREW_NO_AUTO_UPDATE="1"

# add local binaries to PATH if they aren't added yet
# affix colons on either side of $PATH to simplify matching
case ":${PATH}:" in
    *:"$HOME/.local/bin":*)
        ;;
    *)
        # Prepending path in case a system-installed binary needs to be overridden
        export PATH="$HOME/.local/bin:$PATH"
        ;;
esac

