var dagfuncs = (window.dashAgGridFunctions = window.dashAgGridFunctions || {});

dagfuncs.dateFilterComparator = (filterLocalDateAtMidnight, cellValue) => {

    if (cellValue == null) {
        return 0;
    }

    // transaction_time_format = "%d/%m/%y %H:%M"
    const dateParts = cellValue.split(" ")[0].split("/");
    const year = Number("20" + dateParts[2]);
    const month = Number(dateParts[1]) - 1;
    const day = Number(dateParts[0]);
    const cellDate = new Date(year, month, day);

    if (cellDate < filterLocalDateAtMidnight) {
        return -1;
    } else if (cellDate > filterLocalDateAtMidnight) {
        return 1;
    }
    return 0;
};

dagfuncs.timedeltaParser = (value) => {

    if (!value) {
        return null;
    }

    let inp = value;

    let timedelta = 0;

    let H = 0;
    let M = 0;
    let y = 0;
    let m = 0;
    let d = 0;

    // durationformat = y + " | " + m + " | " + d + " | " + H + " , " + M
    if (inp.includes("|")) {
      inp = inp.split("|");
      const inpN = inp.slice(-1)[0]
      if (inpN.includes(",")) {
        let HM = inpN.split(",");
        H = HM[0];
        M = HM[1];
        inp.splice(-1, 1)
      }
      y = inp[0];
      m = inp[1];
      d = inp[2];
    }
    else if (inp.includes(",")) {
        let HM = inp.split(",");
        H = HM[0];
        M = HM[1];
    }
    else {
      y = inp
    }

    timedelta = timedelta + (y ? y * 31557600 : 0);
    timedelta = timedelta + (m ? m * 2629800 : 0);
    timedelta = timedelta + (d ? d * 86400 : 0);
    timedelta = timedelta + (H ? H * 3600 : 0);
    timedelta = timedelta + (M ? M * 60 : 0);

    return timedelta;
};


dagfuncs.timedeltaFormatter = (cellValue) => {

    if (!cellValue) {
      return null;
    }

    let timedelta = cellValue;

    let y = ~~(timedelta / 31557600);
    y = y ? y.toString() : '';
    timedelta = timedelta % 31557600;

    let m = ~~(timedelta / 2629800);
    m = m ? m.toString() : '';
    if (m || y) {
      m = ("00" + m).slice(-2)
    }
    timedelta = timedelta % 2629800;

    let d = ~~(timedelta / 86400);
    d = d ? d.toString() : '';
    if (d || m) {
      d = ("00" + d).slice(-2)
    }
    timedelta = timedelta % 86400;

    let H = ~~(timedelta / 3600);
    H = H ? H.toString() : '';
    if (H || d) {
      H = ("00" + H).slice(-2)
    }
    timedelta = timedelta % 3600;

    let M = ("00" + (~~(timedelta / 60)).toString()).slice(-2);

    // durationformat = y + " | " + m + " | " + d + " | " + H + " , " + M
    const timedeltaString = y + " | " + m + " | " + d + " | " + H + " , " + M;

    return timedeltaString;
};