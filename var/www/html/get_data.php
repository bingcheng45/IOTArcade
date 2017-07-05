<?php
header('Access-Control-Allow-Origin: *'); 

  $data = array();
  
  try {
  
    $mysqli = new mysqli('localhost','assignmentuser','123456','CA1Database');
$query = "SELECT DATE(dateTimeInfo),HOUR(dateTimeInfo), COUNT(*) FROM arcadeData GROUP BY HOUR(dateTimeInfo) ORDER BY dateTimeInfo ASC ";
      
    if ($stmt = $mysqli->prepare($query)) {
        $stmt->execute();
	$stmt->bind_result($dateTimeInfo,$hour,$count);           
        
        while (mysqli_stmt_fetch($stmt)) {		
           $datarow = array("Time"=>$dateTimeInfo,"Hour"=>$hour,"Count"=>$count);
            array_push($data, $datarow);
        } //end while
        
        echo json_encode($data);
        mysqli_stmt_free_result($stmt);
        $stmt->close();
      } //end if $stmt = $mysqli->prepare($query))
  } //end try
  catch (Exception $exception){
      echo $exception;
  } //end catch
?>

