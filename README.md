# UAVproj
### ✅ `README.md`

```markdown
# UAV SAT Path Validator

A Python-based SAT (Boolean Satisfiability) engine that verifies the safety and legality of unmanned aerial vehicle (UAV) flight paths based on airspace rules, weather conditions, drone configuration, and restricted zones.

Built using the `python-sat` library (with Glucose3 solver), this tool helps validate whether a UAV flight path is compliant with various constraints, and provides reasons for invalid paths.

---

## 🚀 Features

- Path intersection detection with:
  - Airport no-fly zones
  - Military zones
  - Critical infrastructure
- Altitude rule enforcement (including FAA ceiling)
- Visual Line-of-Sight (VLOS) and BVLOS configuration
- Weather constraint validation (rain, fog, wind, daylight)
- Drone classification (small vs large) and airspace type
- Boolean SAT reasoning using Glucose3
- Flexible CLI using `argparse`

---

## 🧪 Example Usage

Run the script with CLI arguments:

```bash
python3 uav_validator.py \
  --path "[(0,0), (1,1), (2,2), (2,3), (3,3)]" \
  --altitudes "[100, 110, 115, 105, 100]" \
  --max_altitude 120 \
  --no_fly_airports "[(2,3),(4,1)]" \
  --vlos_required
```

---

## 📝 Arguments

| Argument               | Type      | Description                                  |
|------------------------|-----------|----------------------------------------------|
| `--path`               | list      | List of (x,y) tuples for the UAV path        |
| `--altitudes`          | list      | List of altitudes for each path point        |
| `--max_altitude`       | int       | Maximum allowed altitude (e.g. 120)          |
| `--no_fly_airports`    | list      | List of (x,y) tuples for airport NFZs        |
| `--no_fly_military`    | list      | List of (x,y) tuples for military NFZs       |
| `--no_fly_infra`       | list      | List of (x,y) tuples for infrastructure NFZs |
| `--rain`               | flag      | If set, simulates rainy weather              |
| `--fog`                | flag      | If set, simulates fog conditions             |
| `--wind`               | flag      | If set, simulates high winds                 |
| `--night`              | flag      | If set, simulates flying at night            |
| `--vlos_required`      | flag      | Require visual line of sight (VLOS)          |
| `--bvlos_allowed`      | flag      | Allow beyond visual line of sight (BVLOS)    |
| `--drone_size`         | string    | `small` or `large` drone                     |
| `--controlled_airspace`| flag      | Indicates flight enters controlled airspace  |

---

## ✅ Output

You’ll receive either:

```text
Output: SAT
```

Or, if the path is invalid:

```text
Output: UNSAT
Reason: Path intersects no-fly zone at (2, 3) (airport)
Reason: VLOS required and BVLOS not allowed
```

---

## 🔧 Requirements

- Python 3.6+
- `python-sat`:

```bash
pip install python-sat[pblib,aiger]
```

---

## 📁 File Structure

```
.
├── uav_validator.py            # Main script (contains UAVSATValidator class + CLI)
├── README.md          # This file
```

---

## 📌 Notes

- Make sure your input path and altitude lists are the same length.
- Paths are evaluated against all defined constraints.
- You can extend this tool by adding new logical constraints in `get_global_constraints()` and trigger logic in `encode_dynamic_conditions()`.

---

## 👨‍💻 Author

Developed by Kyle Bonvillain, Frank Dadzie, Justin Williams for CCIS671 – Cyber-Physical Systems
```
