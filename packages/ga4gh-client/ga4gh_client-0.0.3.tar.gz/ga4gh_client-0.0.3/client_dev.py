"""
Simple shim for running the client program during development.
"""
import ga4gh.client.cli as cli

if __name__ == "__main__":
    cli.client_main()
