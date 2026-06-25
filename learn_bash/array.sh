#!/bin/bash

read -p NAMEFILE
CURRENT_DIR=$(cat pwd)

if [[ -z $NAMEFILE ]]; then
  echo "Please input file name first"
  exit 0
else
  if [[ $NAMEFILE != *.sh ]]; then
    FINALNAME="$FINALNAME.sh"
  fi
  
  echo "#!/bin/bash" > "$FILENAME.sh"
  chmod +x "$FILENAME.sh"
  echo "Creating script completed!"
  echo "Saved as $CURRENT_DIR/$FINALNAME"

fi
