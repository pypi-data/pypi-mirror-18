
```python
from mobiledb import get_mobile_info

province, city, isp, code, zipcode, types = get_mobile_info("13916020000")
print(province, city, isp, code, zipcode, types)

info = get_mobile_info("13906900000")
print(info)
```
