<?php
file_put_contents("cache", date("H:i:s"));
echo file_get_contents("cache");

phpinfo();
