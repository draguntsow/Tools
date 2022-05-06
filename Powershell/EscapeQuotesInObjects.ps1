# Takes an array of objects, iterates over properties, determines the String-typed ones and replaces the quote marks " with ' alternative
# This is useful when dealling with malformed outputs from ConvertTo-JSON
# $computers is an input object

$ncomputers = @()
foreach($computer in $computers) {$ncomputer = @{}; foreach($prop in $computer.PSObject.Properties) { if($prop.value -is [String]) {$ncomputer[$prop.name]=$prop.value.replace("`"", "'")} else {$ncomputer[$prop.name] = $prop.value} } $ncomputers+=$ncomputer}
$ncomputers
