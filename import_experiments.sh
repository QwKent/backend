#!/usr/bin/env bash

set -e

DB_FILE="./media.db"

RAW_DIR="./raw_images"

TARGET_BASE="./uploads/public/experiments/images"

QUALITY=80
MAX_SIZE=1400

mkdir -p "$TARGET_BASE"

echo "========================================"
echo "Importing experiment images..."
echo "========================================"

for EXP_DIR in "$RAW_DIR"/*; do

    [ -d "$EXP_DIR" ] || continue

    EXP_ID=$(basename "$EXP_DIR")

    echo ""
    echo "Experiment: $EXP_ID"

    TARGET_DIR="$TARGET_BASE/$EXP_ID"

    #
    # recreate target dir
    #

    rm -rf "$TARGET_DIR"
    mkdir -p "$TARGET_DIR"

    #
    # clear old db rows
    #

    sqlite3 "$DB_FILE" "
    DELETE FROM experiment_images
    WHERE experiment_id='$EXP_ID';
    "

    COUNTER=1

    #
    # process images
    #

    find "$EXP_DIR" -type f | sort -V | while read IMG; do

        EXT="${IMG##*.}"
        EXT=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')

        case "$EXT" in
            jpg|jpeg|png|webp)
                ;;
            *)
                echo "Skipping unsupported file: $IMG"
                continue
                ;;
        esac

        TARGET_FILE="$TARGET_DIR/$COUNTER.webp"

        echo "Converting:"
        echo "  $(basename "$IMG")"
        echo "  -> $COUNTER.webp"

        magick "$IMG" \
            -limit memory 256MiB \
            -limit disk 1GiB \
            -auto-orient \
            -background white \
            -alpha remove \
            -alpha off \
            -resize "${MAX_SIZE}x${MAX_SIZE}>" \
            -strip \
            -quality $QUALITY \
            -define webp:method=6 \
            "$TARGET_FILE"

        #
        # insert into db
        #

        sqlite3 "$DB_FILE" "
        INSERT INTO experiment_images (
            experiment_id,
            image_url,
            sort_order
        )
        VALUES (
            '$EXP_ID',
            '/static/experiments/images/$EXP_ID/$COUNTER.webp',
            $COUNTER
        );
        "

        COUNTER=$((COUNTER + 1))
    done

    echo "Done: $EXP_ID"
done

echo ""
echo "========================================"
echo "ALL DONE"
echo "========================================"