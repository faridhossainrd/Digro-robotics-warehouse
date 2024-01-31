var app = new Vue({
  el: '#app',
  data: {
    scanner: null,
    activeCameraId: null,
    cameras: [],
    scans: []
  },
  mounted: function () {
    var self = this;
    self.scanner = new Instascan.Scanner({ video: document.getElementById('preview'), scanPeriod: 5 });
    self.scanner.addListener('scan', function (content, image) {
      self.scans.unshift({ date: +(Date.now()), content: content });
      //console.log(content);
      document.getElementById("scanname").innerHTML = content;
      postdata(content);
    });
    Instascan.Camera.getCameras().then(function (cameras) {
      self.cameras = cameras;
      if (cameras.length > 0) {
        self.activeCameraId = cameras[0].id;
        self.scanner.start(cameras[0]);
      } else {
        console.error('No cameras found.');
      }
    }).catch(function (e) {
      console.error(e);
    });
  },
  methods: {
    formatName: function (name) {
      return name || '(unknown)';
    },
    selectCamera: function (camera) {
      this.activeCameraId = camera.id;
      this.scanner.start(camera);
    }
  }
});

function postdata(result)
{
 
	$.ajax({
		type: "POST",
		url: "/load/getitem",
		data: { csrfmiddlewaretoken: document.getElementById("crf2").className ,"id":result},  
		success: function(data) {
      //
      porto = window.location.protocol;
      host = window.location.hostname;
      port = window.location.port;

      link = porto+"//"+host+":"+port+"/media/"+data
      //console.log(link)
      document.getElementById('imgget').src = link;
      
		}
  });

  $.ajax({
		type: "POST",
		url: "/load/getitem1",
		data: { csrfmiddlewaretoken: document.getElementById("crf2").className ,"id":result},  
		success: function(data) {
      document.getElementById('nameitem').innerHTML =data;
		}
  });
  


}