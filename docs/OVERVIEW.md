# Architecture Overview

Ports & Adapters:
- **Core**: domain + application services (pure Python)
- **Adapters**: Flask first (default), others on demand (must preserve core contracts)

This repo is the foundation for building or migrating tools into a Soft Code structure. It is the starting point for program creation and future unification.
