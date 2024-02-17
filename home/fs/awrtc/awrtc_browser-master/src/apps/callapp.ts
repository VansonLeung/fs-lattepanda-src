/*
Copyright (c) 2019, because-why-not.com Limited
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

import * as awrtc from "../awrtc/index"
import { ConnectionId } from "../awrtc/index";

/**
 * Main (and most complicated) example for using BrowserWebRtcCall.
 * Have a look at examples.html for easier scenarios.
 *
 *
 *
 * Features:
 * - Build a "Join" system on top of the regular Listen / Call model to make it easier to use.
 * - basic user interface (This is for easy testing not for use as a final application!!! Write your own using the API)
 * - setup to be compatible with the Unity Asset's CallApp (but without TURN server!)
 * - Get parameters from the address line to configure the call
 * - autostart the call (this might not work in all browsers. Mostly used for testing)
 * Todo:
 * - text message system (so far it sends back the same message)
 * - conference call support
 *
 *
 */
import { DeviceApi } from "../awrtc/media_browser/DeviceApi";


export class CallApp
{
    private mAddress;
    private mNetConfig = new awrtc.NetworkConfig();
    private mCall : awrtc.BrowserWebRtcCall = null;

    //update loop
    private mIntervalId:any = -1;

    private mLocalVideo: HTMLVideoElement = null;
    private mRemoteVideo = {};

    public mVideoMediaList = [];
    public mVideoSizeList = [
        {width: 3840, height: 2160, fps: 60, label: "3840 x 2160 x 60 (4K)"},
        {width: 3840, height: 2160, fps: 30, label: "3840 x 2160 x 30 (4K)"},
        {width: 1920, height: 1080, fps: 60, label: "1920 x 1080 x 60 (1080p)"},
        {width: 1920, height: 1080, fps: 30, label: "1920 x 1080 x 30 (1080p)"},
        // {width: 1280, height: 720, fps: 60, label: "1280 x 720 x 60 (720p)"},
        // {width: 1280, height: 720, fps: 30, label: "1280 x 720 x 30 (720p)"},
        // {width: 640, height: 480, fps: 60, label: "640 x 480 x 60 (480p)"},
        // {width: 640, height: 480, fps: 30, label: "640 x 480 x 30 (480p)"},
    ]

    private mIsRunning = false;

    public constructor()
    {
        this.mNetConfig.IceServers = [
            {urls: "stun:stun.because-why-not.com:443"},
            {urls: "stun:stun.l.google.com:19302"}
        ];
        //use for testing conferences
        //this.mNetConfig.IsConference = true;
        //this.mNetConfig.SignalingUrl = "wss://signaling.because-why-not.com/testshared";
        this.mNetConfig.IsConference = true;
        var hostname = window.location.hostname;
        this.mNetConfig.SignalingUrl = `wss://${hostname}:3000/conferenceapp`;
    }



    private GetParameterByName(name) {
        var url = window.location.href;
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"), results = regex.exec(url);
        if (!results)
            return null;
        if (!results[2])
            return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }
    private tobool(value, defaultval)
    {
        if(value === true || value === "true")
            return true;
        if(value === false || value === "false")
            return false;

        return defaultval;
    }



    public VerifyVideoMedia = () =>
    {
        var self = this;
        navigator.mediaDevices.getUserMedia({
            video: {
                mandatory: {
                    minWidth: 1920,
                    minHeight: 1080,
                },
            },
            audio: true,
        } as MediaStreamConstraints)
            .then(function(stream) {
                console.log(stream);
                console.log(stream.getTracks());
                console.log(stream.getAudioTracks());
                console.log(stream.getVideoTracks());

                var videoTracks = stream.getVideoTracks();
                for (var m in videoTracks)
                {
                    self.mVideoMediaList.push(videoTracks[m])
                }

                var select = self.mUiSelectVideoSource;
                if (select)
                {
                    var child = select.lastElementChild;
                    while (child) {
                        select.removeChild(child);
                        child = select.lastElementChild;
                    }
                }

                for (m in self.mVideoMediaList)
                {
                    var opt = document.createElement("option");
                    opt.value = self.mVideoMediaList[m].label;
                    opt.innerHTML = self.mVideoMediaList[m].label; // whatever property it has
                    select.appendChild(opt);
                }
            })

            .catch(function(error) {
                console.log(error);
                console.error(error);
            })
    }


    public RequestPermission = () => {
        navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true,
        } as MediaStreamConstraints)
            .then(function() {

                console.log('getUserMedia completed successfully.');
                // alert('getUserMedia completed successfully.')

            })

            .catch(function(error) {

                console.log(error.name + ": " + error.message);
                alert(error.name + ": " + error.message)

            });
    }


    public RefreshVideoMediaOptions = () =>
    {
        var self = this;
        self.mVideoMediaList.length = 0;


        var select = self.mUiSelectVideoSource;
        if (select)
        {
            var child = select.lastElementChild;
            while (child) {
                select.removeChild(child);
                child = select.lastElementChild;
            }
        }




        var child = this.mUiSelectVideoSize.lastElementChild;
        while (child) {
            this.mUiSelectVideoSize.removeChild(child);
            child = this.mUiSelectVideoSize.lastElementChild;
        }
        for (var k in this.mVideoSizeList)
        {
            var opt = document.createElement("option");
            opt.value = this.mVideoSizeList[k].label;
            opt.innerHTML = this.mVideoSizeList[k].label;
            self.mUiSelectVideoSize.appendChild(opt);
        }


        if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
            console.log("enumerateDevices() not supported.");
            return;
        }
        navigator.mediaDevices.enumerateDevices()
            .then(function(devices) {
                devices.forEach(function(device) {
                    console.log(device.kind + ": " + device.label +
                        " id = " + device.deviceId);

                    if (device.kind !== 'videoinput')
                    {
                        return;
                    }

                    self.mVideoMediaList.push(device);

                    var opt = document.createElement("option");
                    opt.value = device.deviceId;
                    opt.innerHTML = device.label; // whatever property it has
                    select.appendChild(opt);
                });
            })
            .catch(function(err) {
                console.log(err.name + ": " + err.message);
            });

        /*
        navigator.mediaDevices.getUserMedia({
            video: {
                mandatory: {
                    minWidth: 1920,
                    minHeight: 1080,
                },
            },
            audio: true,
        } as MediaStreamConstraints)
            .then(function(stream) {
                console.log(stream);
                console.log(stream.getTracks());
                console.log(stream.getAudioTracks());
                console.log(stream.getVideoTracks());

                var videoTracks = stream.getVideoTracks();
                for (var m in videoTracks)
                {
                    self.mVideoMediaList.push(videoTracks[m])
                }

                var select = self.mUiSelectVideoSource;
                if (select)
                {
                    var child = select.lastElementChild;
                    while (child) {
                        select.removeChild(child);
                        child = select.lastElementChild;
                    }
                }

                for (m in self.mVideoMediaList)
                {
                    var opt = document.createElement("option");
                    opt.value = self.mVideoMediaList[m].label;
                    opt.innerHTML = self.mVideoMediaList[m].label; // whatever property it has
                    select.appendChild(opt);
                }
            })

            .catch(function(error) {
                console.log(error);
                console.error(error);
            })
            */
    }



    public Start(address, audio, video) : void
    {
        var videoDeviceId = this.mUiSelectVideoSource.value;
        if (!videoDeviceId)
        {
            alert("Please select video device");
            return;
        }


        var video_size = this.mUiSelectVideoSize.value;
        if (!video_size)
        {
            alert("Please select video size");
            return;
        }


        var video_width = 1920;
        var video_height = 1080;
        var video_fps = 30;
        for (var k in this.mVideoSizeList)
        {
            if (this.mVideoSizeList[k].label === video_size)
            {
                video_width = this.mVideoSizeList[k].width;
                video_height = this.mVideoSizeList[k].height;
                video_fps = this.mVideoSizeList[k].fps;
                break;
            }
        }



        if(this.mCall != null)
            this.Stop();

        this.mIsRunning = true;
        this.Ui_OnStart()
        console.log("start");
        console.log("Using signaling server url: " + this.mNetConfig.SignalingUrl);

        //create media configuration
        var config = new awrtc.MediaConfig();
        config.Audio = audio;
        config.Video = video;
        config.IdealWidth = video_width;
        config.IdealHeight = video_height;
        config.IdealFps = video_fps;
        config.VideoDeviceId = videoDeviceId;

        //For usage in HTML set FrameUpdates to false and wait for  MediaUpdate to
        //get the VideoElement. By default awrtc would deliver frames individually
        //for use in Unity WebGL
        console.log("requested config:" + JSON.stringify(config));
        //setup our high level call class.
        this.mCall = new awrtc.BrowserWebRtcCall(this.mNetConfig);

        //handle events (get triggered after Configure / Listen call)
        //+ugly lambda to avoid loosing "this" reference
        this.mCall.addEventListener((sender, args)=>{
            this.OnNetworkEvent(sender, args);
        });



        //As the system is designed for realtime graphics we have to call the Update method. Events are only
        //triggered during this Update call!
        this.mIntervalId = setInterval(()=>{
            this.Update();
        }, 50);


        //configure media. This will request access to media and can fail if the user doesn't have a proper device or
        //blocks access
        this.mCall.Configure(config);

        //Try to listen to the address
        //Conference mode = everyone listening will connect to each other
        //Call mode -> If the address is free it will wait for someone else to connect
        //          -> If the address is used then it will fail to listen and then try to connect via Call(address);
        this.mCall.Listen(address);

    }



    public Stop(): void
    {
        this.Cleanup();
    }

    private Cleanup():void{

        if(this.mCall != null)
        {
            this.mCall.Dispose();
            this.mCall = null;
            clearInterval(this.mIntervalId);
            this.mIntervalId = -1;
            this.mIsRunning = false;
            this.mLocalVideo = null;
            this.mRemoteVideo = {};
            this.mVideoMediaList = [];
        }
        this.Ui_OnCleanup();
    }

    private Update():void
    {
        if(this.mCall != null)
            this.mCall.Update();
    }

    private OnNetworkEvent(sender: any, args: awrtc.CallEventArgs):void{

        //User gave access to requested camera/ microphone
        if (args.Type == awrtc.CallEventType.ConfigurationComplete){
            console.log("configuration complete");
        }
        else if (args.Type == awrtc.CallEventType.MediaUpdate) {

            let margs = args as awrtc.MediaUpdatedEventArgs;
            if (this.mLocalVideo == null && margs.ConnectionId == awrtc.ConnectionId.INVALID) {

                var videoElement = margs.VideoElement;
                this.mLocalVideo = videoElement;
                this.Ui_OnLocalVideo(videoElement);
                console.log("local video added resolution:" + videoElement.videoWidth  + videoElement.videoHeight + " fps: ??");
            }
            else if (margs.ConnectionId != awrtc.ConnectionId.INVALID && this.mRemoteVideo[margs.ConnectionId.id] == null) {

                var videoElement = margs.VideoElement;
                this.mRemoteVideo[margs.ConnectionId.id] = videoElement;
                this.Ui_OnRemoteVideo(videoElement, margs.ConnectionId);
                console.log("remote video added resolution:" + videoElement.videoWidth  + videoElement.videoHeight + " fps: ??");
            }
        }
        else if (args.Type == awrtc.CallEventType.ListeningFailed) {
            //First attempt of this example is to try to listen on a certain address
            //for conference calls this should always work (expect the internet is dead)
            if (this.mNetConfig.IsConference == false) {
                //no conference call and listening failed? someone might have claimed the address.
                //Try to connect to existing call
                this.mCall.Call(this.mAddress);
            }
            else {
                let errorMsg = "Listening failed. Offline? Server dead?";
                console.error(errorMsg);
                this.Ui_OnError(errorMsg);
                this.Cleanup();
                return;
            }
        }
        else if (args.Type == awrtc.CallEventType.ConnectionFailed) {
            //Outgoing call failed entirely. This can mean there is no address to connect to,
            //server is offline, internet is dead, firewall blocked access, ...
            let errorMsg = "Connection failed. Offline? Server dead? ";
            console.error(errorMsg);
            this.Ui_OnError(errorMsg);
            this.Cleanup();
            return;
        }
        else if (args.Type == awrtc.CallEventType.CallEnded) {
            //call ended or was disconnected
            var callEndedEvent = args as awrtc.CallEndedEventArgs;
            console.log("call ended with id " + callEndedEvent.ConnectionId.id);
            delete this.mRemoteVideo[callEndedEvent.ConnectionId.id];
            this.Ui_OnLog("Disconnected from user with id " + callEndedEvent.ConnectionId.id);
            //check if this was the last user
            if(this.mNetConfig.IsConference == false && Object.keys(this.mRemoteVideo).length == 0)
            {
                //1 to 1 call and only user left -> quit
                this.Cleanup();
                return;
            }
        }
        else if (args.Type == awrtc.CallEventType.Message) {
            //no ui for this yet. simply echo messages for testing
            let messageArgs = args as awrtc.MessageEventArgs;
            this.mCall.Send(messageArgs.Content, messageArgs.Reliable, messageArgs.ConnectionId);
        }
        else if (args.Type == awrtc.CallEventType.DataMessage) {
            //no ui for this yet. simply echo messages for testing
            let messageArgs = args as awrtc.DataMessageEventArgs;
            this.mCall.SendData(messageArgs.Content, messageArgs.Reliable, messageArgs.ConnectionId);
        }
        else {
            console.log("Unhandled event: " + args.Type);
        }
    }


    //UI calls. should be moved out into its own class later
    private mAudio;
    private mVideo;
    private mVideoDeviceName;
    private mAutostart;
    private mUiAddress: HTMLInputElement;
    private mUiAudio: HTMLInputElement;
    private mUiVideo: HTMLInputElement;
    private mUiButton: HTMLButtonElement;
    private mUiSelectVideoSource: HTMLSelectElement;
    private mUiSelectVideoSourceButton: HTMLButtonElement;
    private mUiRequestPermissionButton: HTMLButtonElement;
    private mUiSelectVideoSize: HTMLSelectElement;
    private mUiUrl: HTMLElement;
    private mUiLocalVideoParent: HTMLElement;
    private mUiRemoteVideoParent: HTMLElement;

    public setupUi(parent : HTMLElement)
    {
        this.mUiAddress = parent.querySelector<HTMLInputElement>(".callapp_address");
        this.mUiAudio = parent.querySelector<HTMLInputElement>(".callapp_send_audio");
        this.mUiVideo = parent.querySelector<HTMLInputElement>(".callapp_send_video");
        this.mUiUrl = parent.querySelector<HTMLParagraphElement>(".callapp_url");
        this.mUiButton = parent.querySelector<HTMLInputElement>(".callapp_button");
        this.mUiLocalVideoParent =  parent.querySelector<HTMLParagraphElement>(".callapp_local_video");
        this.mUiRemoteVideoParent =  parent.querySelector<HTMLParagraphElement>(".callapp_remote_video");
        this.mUiSelectVideoSource =  parent.querySelector<HTMLSelectElement>("#select_video_source");
        this.mUiSelectVideoSourceButton =  parent.querySelector<HTMLInputElement>("#select_video_source_refresh");
        this.mUiRequestPermissionButton =  parent.querySelector<HTMLInputElement>("#request_permission");
        this.mUiRequestPermissionButton.onclick = this.RequestPermission;
        this.mUiSelectVideoSize =  parent.querySelector<HTMLSelectElement>("#select_video_size");
        this.mUiSelectVideoSourceButton.onclick = this.RefreshVideoMediaOptions;
        this.mUiAudio.onclick = this.Ui_OnUpdate;
        this.mUiVideo.onclick = this.Ui_OnUpdate;
        this.mUiAddress.onkeyup = this.Ui_OnUpdate;
        this.mUiButton.onclick = this.Ui_OnStartStopButtonClicked;

        //set default value + make string "true"/"false" to proper booleans
        this.mAudio = this.GetParameterByName("audio");
        this.mAudio  = this.tobool(this.mAudio , true)

        this.mVideo  = this.GetParameterByName("video");
        this.mVideo  = this.tobool(this.mVideo , true);

        this.mAutostart = this.GetParameterByName("autostart");
        this.mAutostart = this.tobool(this.mAutostart, false);
        this.mAddress = this.GetParameterByName("a");


        //if autostart is set but no address is given -> create one and reopen the page
        if (this.mAddress === null && this.mAutostart == true) {
            this.mAddress = this.GenerateRandomKey();
            window.location.href = this.GetUrlParams();
        }
        else
        {
            if(this.mAddress === null)
                this.mAddress = this.GenerateRandomKey();
                this.Ui_Update();
        }

        //used for interacting with the Unity CallApp

        //current hack to get the html element delivered. by default this
        //just the image is copied and given as array
        //Lazy frames will be the default soon though


        if(this.mAutostart)
        {
            console.log("Starting automatically ... ")
            this.Start(this.mAddress, this.mAudio , this.mVideo);
        }

        console.log("address: " + this.mAddress + " audio: " + this.mAudio  + " video: " + this.mVideo + " this.mVideoDeviceName: " + this.mVideoDeviceName  + " autostart: " + this.mAutostart);
    }
    private Ui_OnStart(){
        this.mUiButton.textContent = "Stop";
    }
    private Ui_OnCleanup()
    {
        this.mUiButton.textContent = "Join";
        while (this.mUiLocalVideoParent.hasChildNodes()) {
            this.mUiLocalVideoParent.removeChild(this.mUiLocalVideoParent.firstChild);
        }
        while (this.mUiRemoteVideoParent.hasChildNodes()) {
            this.mUiRemoteVideoParent.removeChild(this.mUiRemoteVideoParent.firstChild);
        }
    }
    private Ui_OnLog(msg:string){

    }
    private Ui_OnError(msg:string){

    }
    private Ui_OnLocalVideo(video : HTMLVideoElement){
        this.mUiLocalVideoParent.appendChild( document.createElement("br"));
        this.mUiLocalVideoParent.appendChild(new Text(video.videoWidth + " x " + video.videoHeight));
        this.mUiLocalVideoParent.appendChild(video);
        var btn = document.createElement('div');
        btn.style.background = "#ddd";
        btn.onclick = () => {
            video.style.objectFit = "fill";
            video.style.position = 'fixed';
            video.style.width = '100%';
            video.style.height = '100%';
            video.style.left = '0';
            video.style.top = '0';
            video.style.bottom = '0';
            video.style.right = '0';
        };
        video.onclick = () => {
            video.style.objectFit = 'contain';
            video.style.position = 'relative';
            video.style.width = '320px';
            video.style.height = '240px';
            video.style.left = '0';
            video.style.top = '0';
            video.style.bottom = '0';
            video.style.right = '0';
        };
        btn.innerText = "Fullscreen";
        this.mUiLocalVideoParent.appendChild(btn);
    }

    private Ui_OnRemoteVideo(video : HTMLVideoElement, id: ConnectionId){

        this.mUiRemoteVideoParent.appendChild( document.createElement("br"));
        this.mUiRemoteVideoParent.appendChild(new Text("connection " + id.id));
        this.mUiRemoteVideoParent.appendChild(new Text(video.videoWidth + " x " + video.videoHeight));
        this.mUiRemoteVideoParent.appendChild( document.createElement("br"));
        this.mUiRemoteVideoParent.appendChild(video);
        var btn = document.createElement('div');
        btn.style.background = "#ddd";
        btn.onclick = () => {
            video.style.objectFit = "fill";
            video.style.position = 'fixed';
            video.style.width = '100%';
            video.style.height = '100%';
            video.style.left = '0';
            video.style.top = '0';
            video.style.bottom = '0';
            video.style.right = '0';
        };
        video.onclick = () => {
            video.style.objectFit = 'contain';
            video.style.position = 'relative';
            video.style.width = '320px';
            video.style.height = '240px';
            video.style.left = '0';
            video.style.top = '0';
            video.style.bottom = '0';
            video.style.right = '0';
        };
        btn.innerText = "Fullscreen";
        this.mUiRemoteVideoParent.appendChild(btn);
    }

    public Ui_OnStartStopButtonClicked = ()=>{
        if(this.mIsRunning) {

            this.Stop();
        }else{
            this.Start(this.mAddress, this.mAudio, this.mVideo);
        }

    }
    public Ui_OnUpdate = ()=>
    {
        console.debug("OnUiUpdate");
        this.mAddress = this.mUiAddress.value;
        this.mAudio  = this.mUiAudio.checked;
        this.mVideo  = this.mUiVideo.checked;
        this.mUiUrl.innerHTML = this.GetUrl();
    }

    public Ui_Update() : void
    {
        console.log("UpdateUi");
        this.mUiAddress.value = this.mAddress;
        this.mUiAudio.checked = this.mAudio ;
        this.mUiVideo.checked = this.mVideo ;
        this.mUiUrl.innerHTML = this.GetUrl();
    }


    private GenerateRandomKey() {
        var result = "";
        for (var i = 0; i < 7; i++) {
            result += String.fromCharCode(65 + Math.round(Math.random() * 25));
        }
        return result;
    }
    private GetUrlParams() {
        return "?a=" + this.mAddress + "&audio=" + this.mAudio  + "&video=" + this.mVideo  + "&" + "autostart=" + true;
    }
    private GetUrl() {
        return location.protocol + '//' + location.host + location.pathname + this.GetUrlParams();
    }
}



export function callapp(parent: HTMLElement)
{
    let callApp : CallApp;
    console.log("init callapp");
    if(parent == null)
    {
        console.log("parent was null");
        parent = document.body;
    }
    awrtc.SLog.SetLogLevel(awrtc.SLogLevel.Info);
    callApp = new CallApp();
    callApp.setupUi(parent);
    callApp.RefreshVideoMediaOptions();
}
