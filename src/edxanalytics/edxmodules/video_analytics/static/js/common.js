/* Helper Functions */

/* Return the size of an object, because .length doesn't work for objects */
function getObjectSize(obj){
    var size = 0;
    var key;
    for (key in obj){
        if (obj.hasOwnProperty(key))
            size++;
    }
    return size;
}


/* Return a human-readable format for the number of seconds */
function formatSeconds(sec){
    var s = Math.round(sec%60);
    return "" + Math.floor(sec/60) + ":" + (s<=9 ? '0' + s : s);
}
