$(function () {
    var $startTime = $('#startTime');
    var $relative = $('#relative');
    var $stopTime = $('#stopTime');
    var $start = $('#start');
    var $pause = $('#pause');
    var $stop = $('#stop');
    var $step = $('#step');
    var $steps = $('#steps');
    var timeFormat = 'H:mm:ss';

    var dateZero = new Date();
    dateZero.setHours(0);
    dateZero.setMinutes(0);
    dateZero.setSeconds(0);
    dateZero.setMilliseconds(0);
    dateZero = dateZero.getTime();

    // Create my chronometer instance
    var chronometer = new Chronometer();

    // When start, update the DOM startTime
    chronometer.addEventListener('started', function () {
        var humanTime = moment(this.startTime).format(timeFormat);
        humanTime = '20:45:12';
        $startTime.text(humanTime);
        $stopTime.text('');
        $relative.text('');
        if (!this.steps.length) {
            $steps.empty();
        }
    });

    function updateButtons() {
        // Update buttons according to the chronometer state
        var state = this.state;
        $start.prop('disabled', state === Chronometer.prototype.RUNNING);
        $pause.prop('disabled', state !== Chronometer.prototype.RUNNING);
        $stop.prop('disabled', state === Chronometer.prototype.STOPPED);
        $step.prop('disabled', state !== Chronometer.prototype.RUNNING);
    }

    updateButtons.apply(chronometer);

    // When state change, update the buttons
    chronometer.addEventListener('state', updateButtons);

    // When stopped, update the DOM stopTime
    chronometer.addEventListener('stopped', function () {
        var humanTime = moment(this.stopTime).format(timeFormat);
        $stopTime.text(humanTime);
        $relative.text(moment(dateZero + this.elapsedTime).format('HH:mm:ss'));
    });

    // When update delegate to relative DOM element
    chronometer.addEventListener('updated', function () {
        $relative.text(moment(dateZero + this.elapsedTime).format('HH:mm:ss'));
    });

    // Show steps on the DOM
    chronometer.addEventListener('stepinserted', function () {
        var $currentStep = $('<li></li>');

        var elapsed = moment(dateZero + this.elapsedTime).format('HH:mm:ss');
        var date = moment(this.steps[this.steps.length - 1].pauseTime).format(timeFormat);
        $currentStep.text(elapsed + ' at ' + date);
        $steps.append($currentStep);
    });


    // Buttons actions
    $start.on('click', function () {
        chronometer.start();
        $('div#html-editor').editable('enable')
    });
    $pause.on('click', function () {
        chronometer.pause();
        $('div#html-editor').editable('disable')
    });
    $stop.on('click', function () {
        chronometer.stop();
        $('div#html-editor').editable('disable')
    });
    $step.on('click', function () {
        chronometer.step();
    });
    window.chronometer = chronometer;
});
