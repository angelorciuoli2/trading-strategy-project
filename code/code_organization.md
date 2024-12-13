**data\_loader.py**: Responsible for data loading. It stays at the root for easier access.

**ma\_strategy.py**: The base strategy file; it contains common logic for both the EMA and SMA strategies.

**ema.py and sma.py**: These files are strategy-specific subclasses, located next to each other for easy comparison and understanding.

**plot\_utils.py**: Contains plotting functions, placed at the root level for easy access to visualization functions.

**main.py**: This is the entry point for your app, so it should be at the root level as well.
