#!/usr/bin/env python3

import connexion

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/', debug=True)
    app.add_api('swagger.yaml', arguments={'title': 'k2data moduler'})
    app.run(port=8080)
