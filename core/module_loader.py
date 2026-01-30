import pkgutil
import importlib
import sys

def load_modules(app):
    # Ensure the 'modules' directory is importable
    try:
        import modules
    except ImportError as e:
        print(f"❌ Error importing modules package: {e}")
        return

    print("🔍 Scanning modules...")

    # Iterates through folders inside 'modules/'
    for _, name, is_pkg in pkgutil.iter_modules(modules.__path__):
        if is_pkg:
            print(f"➡ Found module: {name}")
            try:
                # Dynamic import: modules.device_observability.init
                module = importlib.import_module(f"modules.{name}.init")
                
                if hasattr(module, "register"):
                    module.register(app)
                else:
                    print(f"   ⚠️ Skipping {name}: No 'register' function found.")
            except Exception as e:
                print(f"   ❌ Failed to load {name}: {e}")