import math

from cleaner import Cleaner


class SupplementsCleaner(Cleaner):
    def __init__(self, filepath):
        super(SupplementsCleaner, self).__init__(filepath)

    def clean(self, obj):
        cleaned_qas = []

        for qa in obj.get("qas", []):
            a = qa.get("a")

            # Skip if 'a' is NaN (string or float nan)
            if a is None or str(a).lower() == "nan":
                continue

            # Try convert to int or float
            if isinstance(a, str):
                try:
                    if "." in a:
                        num = float(a)
                        # round to 2dp
                        num = round(num, 2)
                        # keep as int if it's whole after rounding
                        if num.is_integer():
                            num = int(num)
                        a = num
                    else:
                        a = int(a)
                except ValueError:
                    # not numeric, keep as string
                    pass
            elif isinstance(a, float):
                # Handle real float values
                if math.isnan(a):
                    continue
                a = round(a, 2)
                if a.is_integer():
                    a = int(a)

            qa["a"] = a
            cleaned_qas.append(qa)

        obj["qas"] = cleaned_qas
        return obj