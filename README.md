# UAVproj


## Library Usage

Great — since the import now works, here’s how you can **use your installed `uavsat` package** in two different ways:

---

### ✅ Option 1: As a Python Library

You can import and use it directly:

```python
from uavsat import UAVSATValidator

validator = UAVSATValidator()

result, reasons = validator.validate(
    path=[(0, 0), (1, 1), (2, 2), (3, 3)],
    altitudes=[100, 110, 115, 105],
    max_altitude=120,
    no_fly_zones={
        'airports': [(2, 2)],
        'military': [],
        'infrastructure': []
    },
    weather_flags={
        'rain': False,
        'fog': False,
        'wind': False,
        'daylight': True
    },
    vlos_required=True,
    bvlos_allowed=False,
    drone_size='small',
    controlled_airspace=False
)

print("SAT Query: Is this path valid?")
print("Output:", result)
for reason in reasons:
    print("Reason:", reason)
```

---

### ✅ Option 2: As a CLI Tool (via entry point)

You can run from terminal:

```bash
uavsat \
  --path "[(0,0),(1,1),(2,2),(3,3)]" \
  --altitudes "[100,110,115,105]" \
  --max_altitude 120 \
  --no_fly_airports "[(2,2)]" \
  --vlos_required
```

You can also try:

```bash
uavsat --help
```

to view all the available arguments.


---

## 📌 Notes

- Make sure your input path and altitude lists are the same length.
- Paths are evaluated against all defined constraints.
- You can extend this tool by adding new logical constraints in `get_global_constraints()` and trigger logic in `encode_dynamic_conditions()`.

---

## 👨‍💻 Author

Developed by Kyle Bonvillain, Frank Dadzie, Justin Williams for CCIS671 – Cyber-Physical Systems
