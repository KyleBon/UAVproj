import argparse
import ast

from pysat.solvers import Glucose3

class UAVSATValidator:
    def __init__(self):
        self.vars = {
            'Path_OK': 1,
            'NF_Airports_Triggered': 2,
            'NF_Military_Triggered': 3,
            'NF_Critical_Triggered': 4,
            'A_max': 5,
            'A_400': 6,
            'VLOS_Required': 7,
            'BVLOS_Allowed': 8,
            'Weather_Rain': 9,
            'Weather_Fog': 10,
            'Weather_Wind': 11,
            'Weather_Daylight': 12,
            'Size_Small': 13,
            'Size_Large': 14,
            'Controlled_Airspace': 15,
            'ATC_Coordination': 16
        }

    def get_global_constraints(self):
        v = self.vars
        return [
            [-v['NF_Airports_Triggered'], -v['Path_OK']],
            [-v['NF_Military_Triggered'], -v['Path_OK']],
            [-v['NF_Critical_Triggered'], -v['Path_OK']],
            [-v['A_max'], v['A_400']],
            [-v['VLOS_Required'], -v['BVLOS_Allowed']],
            [-v['Weather_Rain']],
            [-v['Weather_Fog']],
            [-v['Weather_Wind']],
            [-v['Weather_Daylight']],
            [-v['Size_Large'], v['ATC_Coordination']],
            [-v['Controlled_Airspace'], v['ATC_Coordination']]
        ]

    def encode_dynamic_conditions(self, path, altitudes, max_altitude, no_fly_zones,
                                   weather_flags, vlos_required, bvlos_allowed,
                                   drone_size, controlled_airspace):
        v = self.vars
        clauses = []
        violations = []

        # No-fly zones
        airport_hits = [pt for pt in path if pt in no_fly_zones.get('airports', [])]
        if airport_hits:
            clauses.append([v['NF_Airports_Triggered']])
            for pt in airport_hits:
                violations.append(f"Path intersects no-fly zone at {pt} (airport)")
        else:
            clauses.append([-v['NF_Airports_Triggered']])

        military_hits = any(pt in no_fly_zones.get('military', []) for pt in path)
        if military_hits:
            clauses.append([v['NF_Military_Triggered']])
            violations.append("Path intersects military no-fly zone")
        else:
            clauses.append([-v['NF_Military_Triggered']])

        infra_hits = any(pt in no_fly_zones.get('infrastructure', []) for pt in path)
        if infra_hits:
            clauses.append([v['NF_Critical_Triggered']])
            violations.append("Path intersects critical infrastructure no-fly zone")
        else:
            clauses.append([-v['NF_Critical_Triggered']])

        # Altitude
        if any(alt > max_altitude for alt in altitudes):
            clauses.append([-v['A_max']])
            violations.append("Path exceeds maximum altitude")
        else:
            clauses.append([v['A_max']])

        if max_altitude <= 120:
            clauses.append([v['A_400']])

        # VLOS/BVLOS
        clauses.append([v['VLOS_Required']] if vlos_required else [-v['VLOS_Required']])
        clauses.append([v['BVLOS_Allowed']] if bvlos_allowed else [-v['BVLOS_Allowed']])

        if vlos_required and not bvlos_allowed:
            violations.append("VLOS required and BVLOS not allowed")

        # Weather
        if weather_flags.get('rain'):
            clauses.append([v['Weather_Rain']])
            violations.append("Rain present during flight")
        else:
            clauses.append([-v['Weather_Rain']])

        if weather_flags.get('fog'):
            clauses.append([v['Weather_Fog']])
            violations.append("Fog present during flight")
        else:
            clauses.append([-v['Weather_Fog']])

        if weather_flags.get('wind'):
            clauses.append([v['Weather_Wind']])
            violations.append("High wind during flight")
        else:
            clauses.append([-v['Weather_Wind']])

        if not weather_flags.get('daylight', True):
            clauses.append([v['Weather_Daylight']])
            violations.append("Flight attempted in darkness")
        else:
            clauses.append([-v['Weather_Daylight']])

        # Size and airspace
        if drone_size == 'small':
            clauses.append([v['Size_Small']])
            clauses.append([-v['Size_Large']])
        else:
            clauses.append([v['Size_Large']])
            clauses.append([-v['Size_Small']])
            violations.append("Large drone requires ATC coordination")

        if controlled_airspace:
            clauses.append([v['Controlled_Airspace']])
            violations.append("Flight in controlled airspace")
        else:
            clauses.append([-v['Controlled_Airspace']])

        # Test path status
        clauses.append([v['Path_OK']])

        return clauses, violations

    def validate(self, path, altitudes, max_altitude, no_fly_zones,
                 weather_flags, vlos_required=True, bvlos_allowed=False,
                 drone_size='small', controlled_airspace=False):
        solver = Glucose3()
        clauses, violations = self.encode_dynamic_conditions(
            path, altitudes, max_altitude, no_fly_zones, weather_flags,
            vlos_required, bvlos_allowed, drone_size, controlled_airspace
        )
        clauses += self.get_global_constraints()

        for clause in clauses:
            solver.add_clause(clause)

        result = 'SAT' if solver.solve() else 'UNSAT'
        return result, violations if result == 'UNSAT' else []


def main():
    parser = argparse.ArgumentParser(description="UAV SAT Path Validator")

    parser.add_argument("--path", type=str, required=True, help="List of (x,y) tuples. Example: '[(0,0), (1,1), (2,2)]'")
    parser.add_argument("--altitudes", type=str, required=True, help="List of altitudes. Example: '[100,110,120]'")
    parser.add_argument("--max_altitude", type=int, required=True, help="Maximum allowable altitude")

    parser.add_argument("--no_fly_airports", type=str, default="[]", help="List of airport NFZ points")
    parser.add_argument("--no_fly_military", type=str, default="[]", help="List of military NFZ points")
    parser.add_argument("--no_fly_infra", type=str, default="[]", help="List of infrastructure NFZ points")

    parser.add_argument("--rain", action="store_true", help="Flag for rain condition")
    parser.add_argument("--fog", action="store_true", help="Flag for fog condition")
    parser.add_argument("--wind", action="store_true", help="Flag for wind condition")
    parser.add_argument("--night", action="store_true", help="Flag if NOT daylight")

    parser.add_argument("--vlos_required", action="store_true", help="Require VLOS")
    parser.add_argument("--bvlos_allowed", action="store_true", help="Allow BVLOS")
    parser.add_argument("--drone_size", choices=["small", "large"], default="small", help="Drone size")
    parser.add_argument("--controlled_airspace", action="store_true", help="Flag for controlled airspace")

    args = parser.parse_args()

    # Safely evaluate string inputs as Python lists
    path = ast.literal_eval(args.path)
    altitudes = ast.literal_eval(args.altitudes)

    no_fly_zones = {
        'airports': ast.literal_eval(args.no_fly_airports),
        'military': ast.literal_eval(args.no_fly_military),
        'infrastructure': ast.literal_eval(args.no_fly_infra)
    }

    weather_flags = {
        'rain': args.rain,
        'fog': args.fog,
        'wind': args.wind,
        'daylight': not args.night
    }

    validator = UAVSATValidator()

    result, reasons = validator.validate(
        path=path,
        altitudes=altitudes,
        max_altitude=args.max_altitude,
        no_fly_zones=no_fly_zones,
        weather_flags=weather_flags,
        vlos_required=args.vlos_required,
        bvlos_allowed=args.bvlos_allowed,
        drone_size=args.drone_size,
        controlled_airspace=args.controlled_airspace
    )

    print("SAT Query: Is this path valid?")
    print(f"Output: {result}")
    if result == "UNSAT":
        for r in reasons:
            print(f"Reason: {r}")

    '''
    EXAMPLE USAGE:
    python3 test.py   --path "[(0,0), (1,1), (2,2), (2,3), (3,3)]"   --altitudes "[100, 110, 115, 105]"   --max_altitude 120   --no_fly_airports "[(2,3),(4,1)]"   --vlos_required

    
    '''

__all__ = ['UAVSATValidator']