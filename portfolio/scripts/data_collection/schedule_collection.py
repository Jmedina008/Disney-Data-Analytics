"""
Scheduler script for automated data collection.
This script sets up scheduled jobs to run data collection at specified intervals.
"""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from collect_all_data import DataCollector
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_collection_job():
    """Execute the data collection job"""
    logger.info(f"Starting scheduled data collection at {datetime.now()}")
    collector = DataCollector()
    results = collector.run_all_collections()
    
    # Log results
    for service, success in results.items():
        status = "successful" if success else "failed"
        logger.info(f"{service} collection {status}")

def main():
    """Set up and start the scheduler"""
    scheduler = BlockingScheduler()
    
    # Schedule Disney+ content collection (daily at 00:00)
    scheduler.add_job(
        run_collection_job,
        CronTrigger(hour=0, minute=0),
        id='disney_plus_collection',
        name='Daily Disney+ Content Collection'
    )
    
    # Schedule theme park wait times collection (every 15 minutes during park hours)
    scheduler.add_job(
        run_collection_job,
        CronTrigger(
            hour='8-23',  # Park operating hours
            minute='*/15'  # Every 15 minutes
        ),
        id='theme_park_collection',
        name='Theme Park Wait Times Collection'
    )
    
    # Schedule box office data collection (weekly on Monday at 00:00)
    scheduler.add_job(
        run_collection_job,
        CronTrigger(
            day_of_week='mon',
            hour=0,
            minute=0
        ),
        id='box_office_collection',
        name='Weekly Box Office Collection'
    )
    
    logger.info("Starting scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")

if __name__ == "__main__":
    main() 