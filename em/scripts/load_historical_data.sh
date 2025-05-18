#!/bin/bash

# Default values
STOCK=""
ROUTER="SMART"
CURRENCY=""
DURATION="2 Y"
FUNCTION="retrieve"
verbose=false

# Function to display usage
usage() {
  echo "Usage: $0 -s <value> -c <value> [--verbose]"
  echo "Options:"
  echo "  -s, --stock <value>   Value for stock (required)"
  echo "  -r, --router <value>   Value for router (optional, default: SMART)"
  echo "  -d, --duration <value>   Value for duration (optional, default: 2 Y)"
  echo "  -f, --function <value>   Value for function (optional, default: retrieve)"
  echo "  -c, --CURRENCY <value>       Value for currency (required)"
  echo "      --verbose               Enable verbose mode (optional)"
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -s|--stock)
      STOCK="$2"
      shift 2
      ;;
    -r|--router)
      ROUTER="$2"
      shift 2
      ;;
    -d|--duration)
      DURATION="$2"
      shift 2
      ;;
    -f|--function)
      FUNCTION="$2"
      shift 2
      ;;
    -c|--currency)
      CURRENCY="$2"
      shift 2
      ;;
    --verbose)
      verbose=true
      shift
      ;;
    -h|--help)
      usage
      ;;
    -*)
      echo "Unknown option: $1"
      usage
      ;;
    *)
      echo "Unexpected argument: $1"
      usage
      ;;
  esac
done

# -z is zero length
if [[ -z "$STOCK" || -z "$CURRENCY" ]]; then
  echo "Error: Both -s/--stock and -c/--curency are required."
  usage
fi

# Output results
echo "STOCK: $STOCK"
echo "CURRENCY: $CURRENCY"
echo "ROUTER: $ROUTER"
echo "DURATION: $DURATION"
echo "FUNCTION: $FUNCTION"

if $verbose; then
  echo "Verbose mode is ON"
fi

python ../source/tools.py --stock "$STOCK" \
                          --router "$ROUTER" \
                          --currency "$CURRENCY" \
                          --duration "$DURATION" \
                          --function "$FUNCTION"