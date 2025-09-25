#!/usr/bin/env python3
"""
dbt Projects on Snowflake Deployment Script

Performs dbt clean, deps, parse and then uses snow dbt deploy.
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path


def setup_logging(verbose: bool = False):
    """Set up simple colored logging."""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Custom formatter with colors
    class ColorFormatter(logging.Formatter):
        COLORS = {
            'DEBUG': '\033[0;36m[DEBUG]\033[0m',
            'INFO': '\033[0;34m[INFO]\033[0m', 
            'WARNING': '\033[0;33m[WARNING]\033[0m',
            'ERROR': '\033[0;31m[ERROR]\033[0m'
        }
        
        def format(self, record):
            record.levelname = self.COLORS.get(record.levelname, record.levelname)
            return f"{record.levelname} {record.getMessage()}"
    
    logging.basicConfig(level=level, format='%(message)s', handlers=[logging.StreamHandler()])
    logging.getLogger().handlers[0].setFormatter(ColorFormatter())


def run_command(cmd: list, error_msg: str = None) -> None:
    """Run command and exit on failure."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        logging.error(error_msg or f"Command failed: {' '.join(cmd)}")
        sys.exit(1)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Deploy dbt project to Snowflake", add_help=False)
    parser.add_argument("-n", "--name", help="dbt project name")
    parser.add_argument("-c", "--connection", help="Snowflake connection name")
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args, unknown_args = parser.parse_known_args()
    
    setup_logging(args.verbose)
    
    if args.help:
        parser.print_help()
        print("\nAll other arguments are passed directly to 'snow dbt deploy'")
        print("Run 'snow dbt deploy --help' for complete options")
        return
    
    # Get project name
    project_name = args.name or os.getenv('SNOWFLAKE_DBT_PROJECT')
    if not project_name:
        logging.error("Project name required via -n/--name or SNOWFLAKE_DBT_PROJECT env var")
        sys.exit(1)
    
    # Check dependencies
    if not shutil.which("snow"):
        logging.error("Snowflake CLI not found. Install with: pip install snowflake-cli")
        sys.exit(1)
    if not shutil.which("dbt"):
        logging.error("dbt not found. Install with: pip install dbt-core dbt-snowflake")
        sys.exit(1)
    if not Path("deploy_config/profiles.yml").exists():
        logging.error("deploy_config/profiles.yml not found")
        sys.exit(1)
    
    try:
        logging.info(f"Deploying dbt project: {project_name}")
        
        # Test connection if specified
        if args.connection:
            logging.info(f"Testing connection: {args.connection}")
            run_command(["snow", "connection", "test", "-c", args.connection], "Connection test failed")
        
        # Prepare project
        logging.info("Preparing dbt project...")
        run_command(["dbt", "clean"], "dbt clean failed")
        run_command(["dbt", "deps"], "dbt deps failed")
        run_command(["dbt", "parse", "--profiles-dir", "deploy_config"], "dbt parse failed")
        
        # Deploy
        cmd = ["snow", "dbt", "deploy", project_name, "--source", ".", "--profiles-dir", "deploy_config"] + unknown_args
        logging.info(f"Deploying: {' '.join(cmd)}")
        run_command(cmd, "Deployment failed")
        
        logging.info(f"Project '{project_name}' deployed successfully!")
        
        # Show next steps
        conn_flag = f" -c {args.connection}" if args.connection else ""
        print(f"\n\033[0;32mNext Steps:\033[0m")
        print(f"• List projects: snow dbt list{conn_flag}")
        print(f"• Build all: snow dbt execute{conn_flag} {project_name} build")
        print(f"• Run models: snow dbt execute{conn_flag} {project_name} run")
        print(f"• Run tests: snow dbt execute{conn_flag} {project_name} test")
        
    except KeyboardInterrupt:
        logging.warning("Deployment interrupted")
        sys.exit(1)


if __name__ == "__main__":
    main()