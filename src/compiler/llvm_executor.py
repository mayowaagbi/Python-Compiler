from llvmlite import binding
import ctypes

def execute_llvm_ir(llvm_ir):
    """
    Execute the given LLVM IR string by creating an execution engine,
    loading the IR, and running the 'main' function.
    """
    # Step 1: Set up LLVM target and execution engine
    # - Target specifies the machine architecture (from system defaults here)
    # - Target machine compiles and runs LLVM IR code on the current machine
    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()

    # Step 2: Set up an empty backing module for the engine
    # - Used to combine additional modules
    backing_mod = binding.parse_assembly("")
    engine = binding.create_mcjit_compiler(backing_mod, target_machine)

    # Step 3: Parse the LLVM IR code and verify it
    # - Parse the string into an LLVM module
    # - Verifies the IR to ensure it’s valid and ready for execution
    mod = binding.parse_assembly(llvm_ir)
    mod.verify()  # This raises an exception if the IR is invalid

    # Step 4: Add the module to the engine and finalize
    # - Finalizing makes the module executable, loading it into memory
    engine.add_module(mod)
    engine.finalize_object()

    # Step 5: Execute the 'main' function
    # - Retrieve the address of the 'main' function within the IR
    # - Use ctypes to create a callable function in Python
    entry_fn = engine.get_function_address("main")
    main_fn = ctypes.CFUNCTYPE(None)(entry_fn)  # Define the main function as having no arguments or return
    main_fn()  # Execute the 'main' function in the LLVM IR

    print("LLVM IR executed successfully.")
