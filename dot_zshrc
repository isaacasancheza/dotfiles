# enable Powerlevel10k instant prompt
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# path to oh-my-zsh installation
export ZSH="$HOME/.oh-my-zsh"

# zsh theme
ZSH_THEME="powerlevel10k/powerlevel10k"

# update automatically without asking
zstyle ':omz:update' mode auto      

# ssh-agent config
zstyle :omz:plugins:ssh-agent lifetime 4h

# ssh-agent powerlevel10k specific config
zstyle :omz:plugins:ssh-agent quiet yes
zstyle :omz:plugins:ssh-agent lazy yes

# omz plugins
plugins=(uv aws chezmoi ssh-agent auto-notify)

# source omz
source $ZSH/oh-my-zsh.sh

# custom aliases
if [ -f ~/.zsh_aliases ]; then
    source ~/.zsh_aliases
fi

# source powerlevel10k
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

