<?php
require_once __DIR__ . '/_auth.php';
logout();
header('Location: login.php');
exit;
