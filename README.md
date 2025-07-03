# EnvStream

![GitHub release (latest by date)](https://img.shields.io/github/v/release/mjsully/envstream)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/mjsully/envstream)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mjsully/envstream/python-publish.yml)
![GitHub license](https://img.shields.io/github/license/mjsully/envstream)
![GitHub issues](https://img.shields.io/github/issues/mjsully/envstream)

## 📌 Overview

This project provides a database-backed, environmental variables store, enabling on-the-fly app reconfigurations without redeployment!

## 🚀 Features

* Add, update and remove environment variables from code, or from the DB!
* Inferred variable typing

## 📦 Installation

Install the package using pip:
```bash
pip install envstream
```

## 🛠 Usage

Here is an example of using EnvStream:
```python
from envstream import EnvStream

# Create instance of EnvStream
var_handler = EnvStream(
    "Application Name",
    log_level="DEBUG"
)
# Setup DB credentials
var_handler.setup_db(
    username="username",
    password="password",
    host="host",
    port="5432",
    database="database"
)
# Loads variables from DB (WHERE application = 'Application Name')
var_handler.get_variables()
# Set some variables of different types
var_handler.set_variable("variable1", "value") 
var_handler.set_variable("variable2", 1)
var_handler.set_variable("variable3", 1.0)
var_handler.set_variable("variable4", True)
# Update variable by name
var_handler.set_variable("variable4", False)
# Delete variable by name
var_handler.remove_variable("variable4")
# Periodically refresh variables
while True:
    var_handler.refresh()
    time.sleep(5)
# Automatically refresh variables
var_handler.auto_refresh(frequency=5)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 📬 Contact

If you have any questions, feel free to open an issue or reach out via email at [mattys940@gmail.com](mailto:mattys940@gmail.com).
