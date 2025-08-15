<?php

    $data = file_get_contents('validation/data.json');
    $data = json_decode($data, true);
    $authed = false;

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $code = $_POST['code'] ?? '';
        foreach ($data['users'] as &$user) {
            if(isset($user['code']) && $user['code'] == $code) {
                $authed = true;
                header('Content-Type: application/json');

                echo json_encode(array(
                    "code" => 1,
                    "user" => $user['user'],
                    "name" => $user['name'],
                    "message" => "successfully authenticated",
                ));

                unset($user['code']);
                $user['authenticated'] = true;

                file_put_contents('validation/data.json', json_encode($data, JSON_PRETTY_PRINT));
                exit;
            }
        }

        if(!$authed) {
            header('Content-Type: application/json');

            echo json_encode(array(
                "code" => 0,
                "message" => "invalid",
            ));
            exit;
        }

    } else {
        header('Content-Type: application/json');

        echo json_encode(array(
            "code" => 2,
            "message" => "invalid request method",
        ));
        exit;
    }

?>