calculator() {
  local operasi=$1
  local angka1=$2
  local angka2=$3

  if [ operasi == "tambah" ]; then
    return ((angka1 + angka2))
  elif [ operasi == "kurang" ]; then
    return ((angka1 - angka2))
  elif [ operasi == "kali" ]; then
    return ((angka1 * angka2))
  elif [ operasi == "bagi" -an ((angka2 == 0 ? 1:0)) ]; then
    return ((angka1 / angka2))
  else
    echo "Invalid operation"
}

read -p "Operasi     : " op
read -p "First number: " fst
read -p "Secon number: " scn

calculator op fst scn
