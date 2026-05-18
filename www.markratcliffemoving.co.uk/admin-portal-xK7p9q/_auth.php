<?php
/**
 * Auth helpers — session-based login.
 */
require_once __DIR__ . '/_lib.php';

session_start();

function admin_config() {
    $cfg = load_json(CONFIG_FILE, []);
    if (!isset($cfg['admin'])) {
        // First-run defaults — should be replaced via setup
        $cfg['admin'] = [
            'username' => 'mark',
            'password_hash' => '',
        ];
    }
    return $cfg;
}

function is_logged_in() {
    return !empty($_SESSION['admin_user']);
}

function require_login() {
    if (!is_logged_in()) {
        header('Location: login.php');
        exit;
    }
}

function attempt_login($username, $password) {
    $cfg = admin_config();
    if (empty($cfg['admin']['password_hash'])) return false;
    if ($username !== $cfg['admin']['username']) return false;
    if (!password_verify($password, $cfg['admin']['password_hash'])) return false;
    $_SESSION['admin_user'] = $username;
    return true;
}

function logout() {
    session_destroy();
}

function csrf_token() {
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf'];
}

function check_csrf() {
    if (!isset($_POST['csrf']) || !hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'])) {
        die('Invalid CSRF token. Please go back and try again.');
    }
}
