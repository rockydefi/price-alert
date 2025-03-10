The `price-alert.py` script checks the price of a specified cryptocurrency pair and sends a notification via Pushover if the price crosses predefined thresholds.

1. **Set up your `.env` file**: Create a `.env` file in the same directory as `price-alert.py` with your Pushover credentials (you will need Pushover app installed on your phone):
   ```
   PUSHOVER_TOKEN=your_token
   PUSHOVER_USER_KEY=your_user_key
   PUSHOVER_DEVICE_NAME=your_device_name
   PUSHOVER_SOUND=your_sound
   ```

2. **Set up server**: Configure your server (e.g., Hetzner) and set up SSH access.

3. **Transfer files**: Use `scp` to transfer the `.env` and `price-alert.py` files to your server.

4. **Install dependencies**: Ensure the following dependencies are installed and more:
   - `nano`
   - `python`
   - `python-dotenv`

5. **Set up a cron job**: Add a cron job to execute the script at regular intervals. For example:
   ```
   */5 * * * * /usr/bin/python3 /root/price_alert/price-alert.py >> /root/price_alert/cron.log 2>&1
   ```

6. **Script functionality**: The `price-alert.py` script checks the price of a specified cryptocurrency pair and sends a notification via Pushover if the price crosses predefined thresholds.