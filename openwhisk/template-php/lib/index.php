<?php
function main(array $args) : array
{
    $name = $args["name"] ?? "stranger";
    $greeting = "Hello $name!";
    echo $greeting;
    return ["payload" => "Hallo PHP", "htmlText" => "Hallo aus PHP"];
}