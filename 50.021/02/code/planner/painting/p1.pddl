(define (problem p1)
    (:domain painting)
    (:objects a b sprayer red green)
    (:init
        (on a b)
        (on-table b) (on-table sprayer)
        (clear a) (clear sprayer)
        (arm-empty)
        (color-of a red) (color-of b red) (color-of sprayer green)
        (is-obj a) (is-obj b) (is-obj sprayer)
        (is-box a) (is-box b)
        (is-sprayer sprayer)
    )
    (:goal (and
        (color-of b green)
        (on a b)
        (arm-empty)
    ))
)