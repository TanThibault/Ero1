#!/bin/sh
if [ $# -eq 2 ]; then
  if [ $1 = "drone" ]; then
    if [ $2 = "Montreal" ]; then
		python ./vol_drone/drone_montreal.py
    elif [ $2 = "Outremont" ]; then
		python ./vol_drone/drone_outremont.py
	else
		echo "Wrong arguments"
	fi
  elif [ $1 = "deneiger" ]; then
  	if [ $2 = "Outremont" ]; then
		python ./deneigeuse/deneigeuse.py Outremont
	elif [ $2 = "Verdun" ]; then	
		python ./deneigeuse/deneigeuse.py Verdun
	elif [ $2 = "Rivièredesprairiespointeauxtrembles" ]; then	
		python ./deneigeuse/deneigeuse.py Rivière-des-prairies-pointe-aux-trembles
	elif [ $2 = "SaintLéonard" ]; then	
		python ./deneigeuse/deneigeuse.py Saint-Léonard
	elif [ $2 = "PlateauMontRoyal" ]; then	
		python ./deneigeuse/deneigeuse.py Plateau-Mont-Royal
	else
		echo "Wrong arguments"
		echo $2
	fi
  else
	  echo "Wrong arguments"
  fi
else
  echo "Wrong number of args"
fi
