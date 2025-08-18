import cv2
from color import *

DEBUG = False

def get_bb(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)

    # black magic
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    transform = lambda b: tuple([*b[:-1], int(b[-1] * 0.85)])

    bounding_boxes = []

    for _, b in enumerate(map(cv2.boundingRect, contours)): 
        x, y, w, h = b

        if w < 100 or h < 100: # heuristic filter
            continue

        if h > w * 3: # stacks are directly on top of each other
            b1 = (x, y, w, h // 2)
            b2 = (x, y + h // 2, w, h // 2)

            bounding_boxes.append(transform(b1))
            bounding_boxes.append(transform(b2))

        else:
            bounding_boxes.append(transform(b))
    
    # sort by row-wise
    bounding_boxes.sort(key=lambda b: (b[1] // 10, b[0]))

    if DEBUG:
        for i, (x, y, w, h) in enumerate(bounding_boxes, 1):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return bounding_boxes

def get_stacks(img, bounding_boxes):
    bolts = []

    for (x, y, w, h) in bounding_boxes[:-2]:
        seg_h = h // 5

        bolt = []

        # top half of the top nut is about the double the height
        for i in range(1, 5):
            y1 = int(y + i * seg_h)
            y2 = int(y + (i + 1) * seg_h)
            x1 = x
            x2 = x + w

            cx = x1 + (x2 - x1) // 2
            cy = y1 + (y2 - y1) // 2
            
            # get average color in region
            reg = 7
            roi = img[cy - reg : cy + reg, cx - reg : cx + reg, :3]
            b, g, r = roi.mean(axis=(0, 1)).astype(int)

            color = get_color(r, g, b)
            
            bolt.append([*colors.keys()].index(color))
            
            if DEBUG:
                cv2.rectangle(img, (cx - reg, cy - reg), (cx + reg, cy + reg), (0, 0, 255), 2)

        bolts.append(bolt)

    return bolts

def get_puzzle(img_src):
    img = cv2.imread(img_src, cv2.IMREAD_UNCHANGED)

    bolts_bb = get_bb(img)

    puzzle = get_stacks(img, bolts_bb)

    # puzzle always has 2 empty bolts
    for _ in range(2):
        puzzle.append([])

    puzzle = [n[::-1] for n in puzzle]

    if DEBUG:
        cv2.imshow("nuts & bolts", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return puzzle