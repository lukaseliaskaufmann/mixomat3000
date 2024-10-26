BACKGROUND = """background-color: rgb(40, 44, 52);"""

TAB_BUTTON = """
QPushButton {
	background-color:  rgb(33, 37, 43);
	color: rgb(221, 221, 221);
    border: none;
}

QPushButton:pressed {
    border: none;
}

QPushButton:focus {
	background-color: rgb(40, 44, 52);
    color: rgb(113, 126, 149);
    border: none;
	border-left:3px solid rgb(189, 147, 249);
}

QPushButton:hover {
	background-color: rgb(40, 44, 52);
}"""

SLIDER = """
QSlider::groove:vertical {
    border-radius: 5px;
    width: 15 px;
    margin: 0px;
	background-color: rgb(52, 59, 72);
}
QSlider::groove:vertical:hover {
	background-color: rgb(55, 62, 76);
}
QSlider::handle:vertical {
    background-color: rgb(165, 124, 225);
	border: none;
    height: 15 px;
    width: 15 px;
    margin: 0px;
	border-radius: 5px;
}
QSlider::handle:vertical:hover {
    background-color: rgb(195, 155, 255);
}
QSlider::handle:vertical:pressed {
    background-color: rgb(255, 121, 198);
}
QSlider::add-page:vertical {
    background: rgb(189, 147, 249);
	border-radius: 5px;
}
"""

BUTTON = """
QPushButton {
	border: 2px solid rgb(52, 59, 72);
	border-radius: 5px;	
	background-color: rgb(52, 59, 72);
}
QPushButton:hover {
	background-color: rgb(57, 65, 80);
	border: 2px solid rgb(61, 70, 86);
}
QPushButton:pressed {	
	background-color: rgb(35, 40, 49);
	border: 2px solid rgb(43, 50, 61);
}"""

EXIT_BUTTON = """
QPushButton {
	border: 2px solid rgb(52, 59, 72);
	border-radius: 5px;	
	background-color: rgb(52, 59, 72);
}
QPushButton:hover {
	background-color: rgb(220,20,60);
	border: 2px solid rgb(61, 70, 86);
}
QPushButton:pressed {	
	background-color: rgb(220,20,60);
	border: 2px solid rgb(43, 50, 61);
}
"""

DROPDOWN = """
QComboBox{
	background-color: rgb(27, 29, 35);
	border-radius: 5px;
	border: 2px solid rgb(33, 37, 43);
	padding: 5px;
	padding-left: 10px;
}
QComboBox:hover{
	border: 2px solid rgb(64, 71, 88);
}
QComboBox::drop-down {
	subcontrol-origin: padding;
	subcontrol-position: top right;
	width: 25px; 
	border-left-width: 3px;
	border-left-color: rgba(39, 44, 54, 150);
	border-left-style: solid;
	border-top-right-radius: 3px;
	border-bottom-right-radius: 3px;	
	background-image: url(./icons/cil-arrow-bottom.png);
	background-position: center;
	background-repeat: no-reperat;
 }
QComboBox QAbstractItemView {
	color: rgb(255, 121, 198);	
	background-color: rgb(33, 37, 43);
	padding: 5px;
	selection-background-color: rgb(39, 44, 54);
}"""

PROGRESSBAR = """
QProgressBar {
	background-color: rgb(52, 59, 72);
    border-radius: 5px;
    text-align: center;
	height:30px;
}

QProgressBar::chunk {
    background-color: rgb(189, 147, 249);
	border-radius:5px;
}"""

GLASS = """
border-color: black;
border-style: solid;
border-width: 0px 10px 10px 10px;
border-top-left-radius: 0px;
border-top-right-radius: 0px;
border-bottom-right-radius: 20px;
border-bottom-left-radius: 20px;
"""

ALCOHOLIC = """
background: #ba55d3;
border-top-left-radius: 0px;
border-top-right-radius: 0px;
border-bottom-right-radius: 10px;
border-bottom-left-radius: 10px;
"""

SOFT = """
background: #1e90ff;
"""

SOFT_ONLY = """
background: #1e90ff;
border-top-left-radius: 0px;
border-top-right-radius: 0px;
border-bottom-right-radius: 10px;
border-bottom-left-radius: 10px;
"""

PASSWORD = """
QLineEdit {
	width: 25px;
	height: 30px;
    border: 2px solid rgb(33, 37, 43);
    border-radius: 5px;
    background: rgb(27, 29, 35);
    selection-background-color: red;
	color: rgb(255, 121, 198);
	font-size: 20px;
}
"""
