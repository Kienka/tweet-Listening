<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{name}}</title>
    <script src="https://d3js.org/d3.v3.min.js" charset="utf-8"></script>
    <script type="text/javascript" src="{{url_for('static',filename='d3.layout.cloud.js'}}"></script>
    <script type="text/javascript" src="{{url_for('static',filename='tweet_word_cloud.js'}}"></script>
</head>
<body>
<div id="word_cloud"></div>

</body>
</html>