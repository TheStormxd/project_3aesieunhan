<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connect db</title>
</head>
<body>
<table>
  <tr>
    <th> ID</th>
    <th> USERNAME</th>
    <th> PASSWORD</th>
  </tr>
<?php
  $conn = mysqli_connect("localhost", "kienle", "kienle201", "tutor_chatbot");
  if ($conn-> connect_error) {
    die("Connection Failed:". $conn-> connect_error);
  }
  $sql = "SELECT id, username, password from login";
  $result = $conn -> query($sql);

  if ($result-> num_rows >0) {
    while ($row = $result -> fetch_assoc()) {
        echo "<tr><td>". $row["id"] ."<tr><td>". $row["username"] ."<tr><td>". $row["password"] ."<tr><td>".;
    }
    echo "</table>";
  }
  else {
    echo "0 result";
  }

  $conn->close();
?>

  </table>
</body>
</html>