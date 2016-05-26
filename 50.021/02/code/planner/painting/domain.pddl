;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Prodigy blocks world
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain prodigy-bw)
    (:requirements :strips)
    (:predicates (on ?x ?y)
        (on-table ?x)
        (clear ?x)
        (arm-empty)
        (holding ?x)
        (color-of ?x ?color)
        (is-obj ?x)
        (is-box ?x)
        (is-sprayer ?x)
        )
    (:action pick-up
        :parameters (?ob1)
        :precondition (and (clear ?ob1) (on-table ?ob1) (arm-empty) (is-obj ?ob1))
        :effect
        (and (not (on-table ?ob1))
        (not (clear ?ob1))
        (not (arm-empty))
        (holding ?ob1)))
    (:action put-down
        :parameters (?ob)
        :precondition (and (holding ?ob) (is-obj ?ob))
        :effect
        (and (not (holding ?ob))
        (clear ?ob)
        (arm-empty)
        (on-table ?ob)))
    (:action stack
        :parameters (?sob ?sunderob)
        :precondition (and (holding ?sob) (clear ?sunderob) (is-obj ?sob) (is-obj ?sunderob))
        :effect
        (and (not (holding ?sob))
        (not (clear ?sunderob))
        (clear ?sob)
        (arm-empty)
        (on ?sob ?sunderob)))
    (:action unstack
        :parameters (?sob ?sunderob)
        :precondition (and (on ?sob ?sunderob) (clear ?sob) (arm-empty) (is-obj ?sob) (is-obj ?sunderob))
        :effect
        (and (holding ?sob)
        (clear ?sunderob)
        (not (clear ?sob))
        (not (arm-empty))
        (not (on ?sob ?sunderob))))
    (:action spray
    	:parameters (?ob ?sprayer ?color ?boxcolor)
    	:precondition (and (on-table ?ob) (clear ?ob) (color-of ?ob ?boxcolor) (is-box ?ob) (holding ?sprayer) (is-sprayer ?sprayer) (color-of ?sprayer ?color))
    	:effect
    	(and (color-of ?ob ?color)
    	(not (color-of ?ob ?boxcolor))
    	)
    )
)
