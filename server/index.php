<?php
$con = mysqli_connect("compphys2.mysql.domeneshop.no", "compphys", "m5N34WUX", "compphys");

if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT *, TIMESTAMPDIFF(MINUTE, now(), suggestion_time) as eta FROM lunchtime_suggestions HAVING eta > -10 AND eta < 60 ORDER BY suggestion_time DESC");

if(!$result) {
    printf("Errormessage: %s\n", mysqli_error($con));
}

if(isset($_GET["suggest"]) && isset($_GET["username"])) {
    $time = intval($_GET["suggest"]);
    $username = mysqli_real_escape_string($con, $_GET["username"]);

    $result = mysqli_query($con,"INSERT INTO lunchtime_suggestions (suggestion_time, created_time, username) VALUES (NOW() + INTERVAL $time MINUTE, NOW(), '$username')");
    if(!$result) {
        printf("Errormessage: %s\n", mysqli_error($con));
    } else {
        echo "Ok!";
    }
} elseif(isset($_GET["upvote"]) && isset($_GET["suggestion_id"])) {
    $suggestion_id = mysqli_real_escape_string($con, $_GET["suggestion_id"]);

    $result = mysqli_query($con,"UPDATE lunchtime_suggestions SET upvotes=upvotes+1 WHERE suggestion_id=$suggestion_id");
    if(!$result) {
        printf("Errormessage: %s\n", mysqli_error($con));
    } else {
        echo "Ok!";
    }
} else {
    echo "[";
    $first = true;
    while($row = mysqli_fetch_array($result)) {
        if(!$first) {
            echo ",";
        }
        echo "{";
        echo "\"suggestion_id\":\"" . $row['suggestion_id'] . "\",\n";
        echo "\"created_time\":\"" . $row['created_time'] . "\",\n";
        echo "\"time\":\"" . $row['suggestion_time'] . "\",\n";
        echo "\"username\":\"" . $row['username'] . "\",\n";
        echo "\"upvotes\":\"" . $row['upvotes'] . "\",\n";
        echo "\"downvotes\":\"" . $row['downvotes'] . "\",\n";
        echo "\"eta\":\"" . $row['eta'] . "\"\n";
        echo "}";
        $first = false;
    }
    echo "]";
}
?>
