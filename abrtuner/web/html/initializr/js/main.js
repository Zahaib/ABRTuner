$(function() {
    //var AXINOM_DEMO_WV_LS = "http://axpr-wv-fe.cloudapp.net:8080/LicensingService";

    var context = new Dash.di.DashContext();
    var player = new MediaPlayer(context);
    player.startup();
    player.attachView(document.querySelector('#videoPlayer'));
    //player.attachProtectionData({"com.widevine.alpha": new MediaPlayer.vo.protection.ProtectionData(AXINOM_DEMO_WV_LS)});

    $('#playButton').click(function() {
        //var videoUrl = 'http://dash.edgesuite.net/envivio/dashpr/clear/Manifest.mpd';
        var videoUrl = 'http://68.181.99.194/initializr/dashpr/Manifest.mpd';
        //var videoUrl = 'http://68.181.99.194/initializr/simpson/simp-120gop_dash.mpd';
        //var videoUrl = 'http://68.181.99.194/initializr/weird-envivio/Manifest.mpd';
        player.attachSource(videoUrl);
    });
});


//(function(){
//	$('#playButton').click(function() {
//        	var url = "http://68.181.99.194/initializr/dashpr/Manifest.mpd";
//        	var player = dashjs.MediaPlayer().create();
//        	player.initialize(document.querySelector("#videoPlayer"), url, true);
//	});
//})();

