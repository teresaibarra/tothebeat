// taken from https://github.com/UlloLabs/tutorial.HR-WebBLE/tree/master


document.addEventListener('click', () => {
    // Check if the AudioContext is suspended and resume it if necessary
    if (Tone.context.state === 'suspended') {
        Tone.context.resume();
    }
});

//create a synth and connect it to the main output (your speakers)
const synth = new Tone.Synth().toDestination();
//play a middle 'C' for the duration of an 8th note
synth.triggerAttackRelease("C4", "8n");


var BPM = 0.0 ;
var heart = document.getElementById("heartSprite") ;
let p = document.getElementById("dataText") ;
if (navigator.bluetooth === undefined) {
    p.textContent = "Web bluetooth is not supported" ;
}
else {
    let button = document.getElementById("connectButton") ;
    button.style.cursor = "pointer" ;
    handleCharacteristicValueChanged = (event) => {
        let value = event.target.value ; // a dataviewer object is provided by the object event
        let heartrate = value.getUint8(1) ; // we select the eight bytes that contain the heartrate informations
        p.textContent = heartrate + " BPM" ; // and display it
        BPM = heartrate ;
    }
    onClickEvent = () => {
        navigator.bluetooth.requestDevice({ filters: [{ services: ['heart_rate'] }] }) // we filter the devices, displaying only those with heartrate services
        .then(device => device.gatt.connect()) // after the user select a device, we return the selected one
        .then(server => server.getPrimaryService('heart_rate')) // we get the service
        .then(service => service.getCharacteristic('heart_rate_measurement')) // then the characteristics
        .then(characteristic => characteristic.startNotifications())
        .then(characteristic => {          
            characteristic.addEventListener('characteristicvaluechanged', handleCharacteristicValueChanged) ; // then we subscribe to the characteristic notifications
        })                                                                                                    // and set the callback function
        .catch(error => { console.error(error); }) ; // we display the errors on the console
    }
    button.addEventListener('click', onClickEvent ) ;
    let startTime = performance.now() ;
    let step = 0 ;
    updateHeartSize = () => {
        if (BPM > 0)
        {
            let ibi = 60./BPM * 1000 ;
            let elapsedTime = performance.now() - startTime ;
            let scaleUp = 1.1 ;
            let scaleDown = (1/scaleUp).toFixed(2) ;
            if (elapsedTime < ibi * 0.05 && step == 0 )
            {
                step++ ;
                heartSprite.style.transform = "scale(" + scaleUp + ")" ;
            }
            else if ( elapsedTime > ibi * 0.05 && elapsedTime < ibi * 0.22 && step == 1)
            {
                step++ ;
                heartSprite.style.transform = "scale(" + scaleDown + ")" ;
            }
            else if ( elapsedTime > ibi * 0.22 && elapsedTime < ibi * 0.26 && step == 2)
            {
                step++ ;
                heartSprite.style.transform = "scale(" + scaleUp + ")" ;
            }
            else if (elapsedTime > ibi * 0.26 && step == 3)
            {
                step++ ;
                heartSprite.style.transform = "scale(" + scaleDown + ")" ;
            }
            if (elapsedTime > ibi)
            {
                step = 0 ;
                startTime = performance.now() ;
            }
        }
        globalID = requestAnimationFrame(updateHeartSize) ;
    } ;
    let globalID = requestAnimationFrame(updateHeartSize) ;
}