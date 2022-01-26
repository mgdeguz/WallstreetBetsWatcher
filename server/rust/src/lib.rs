extern crate cpython;

use cpython::{PyResult, Python, py_module_initializer, py_fn};

py_module_initializer!(mylib, |py, m| {
    m.add(py, "__doc__", "This module is implemented in Rust.")?;
    m.add(py, "rust_split_str", py_fn!(py, rust_split_str(val: &str)))?;
    Ok(())
});

fn rust_split_str(_py: Python, val: &str) -> PyResult<Vec<String>> {
    let tokens = val.split(" ");
    let x: Vec<String> = tokens.map(|s| s.to_string()).collect();
    return Ok(x);
    // Ok("Rust says: ".to_owned() + val)
}
