#!/usr/bin/env bash
set -euo pipefail

# =========================
# Configuración
# =========================
DOMAIN=""
DOMAIN_OWNER=""
REPOSITORY=""
REGION=""
SCOPE=""
NPMRC="${HOME}/.npmrc"

# =========================
# Obtener token
# =========================
TOKEN="$(
  aws codeartifact get-authorization-token \
    --domain "${DOMAIN}" \
    --domain-owner "${DOMAIN_OWNER}" \
    --region "${REGION}" \
    --query authorizationToken \
    --output text
)"

REGISTRY_URL="https://${DOMAIN}-${AWS_ACCOUNT_ID:-$(aws sts get-caller-identity --query Account --output text)}.d.codeartifact.${REGION}.amazonaws.com/npm/${REPOSITORY}/"

# =========================
# Limpiar entradas previas
# =========================
if [[ -f "${NPMRC}" ]]; then
  sed -i.bak \
    -e "/^${SCOPE}:registry=/d" \
    -e "\|${REGISTRY_URL}:_authToken=|d" \
    "${NPMRC}"
fi

# =========================
# Escribir configuración
# =========================
cat <<EOF >> "${NPMRC}"
${SCOPE}:registry=${REGISTRY_URL}
//$(echo "${REGISTRY_URL}" | sed 's|https://||'):_authToken=${TOKEN}
EOF

echo "Registro de CodeArtifact actualizado para ${SCOPE}"
