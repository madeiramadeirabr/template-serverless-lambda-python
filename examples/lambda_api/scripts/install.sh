if test -f "requirements.txt"; then
  python3 -m pip install -r requirements.txt
fi

if test -f "requirements-vendor.txt"; then
  python3 -m pip install -r requirements-vendor.txt -t ./vendor
fi
