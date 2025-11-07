from procesamiento.install_dependencies import install_packages

def instalarDependencias():
    install_packages()

if __name__ == "__main__":
    instalarDependencias()
    from llamados import mostrar_menu
    mostrar_menu()
