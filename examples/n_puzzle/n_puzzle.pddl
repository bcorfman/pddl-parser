(define (domain n-puzzle)
  (:requirements :strips :typing )

  (:types
    tile  ; puzzles have numbered tiles
    slot  ; each puzzle tile goes in a slot
    dist  ; distance between slots
  )
  (:constants
     T1 T2 T3 T4 T5 T6 T7 T8 Blank - tile
     S1 S2 S3 S4 S5 S6 S7 S8 S9 - slot
  )

  (:predicates
    (adjacent ?s1 ?s2 - slot) ; slot ?s1 is adjacent to ?s2
    (at ?t - tile ?s - slot)  ; tile ?t is at slot ?s
    (equal ?s1 ?s2 - slot)    ; slot ?s1 is equal ?s2
    (distx ?s1 ?s2 - slot ?d - dist)    ; horizontal distance between two slots
    (disty ?s1 ?s2 - slot ?d - dist)    ; vertical distance between two slots
  )

  ; moves a tile between two adjacent slots
  (:action move
    :parameters (?t - tile ?s1 ?s2 - slot)
    :precondition (and (adjacent ?s1 ?s2) (at Blank ?s1) (at ?t ?s2))
    :effect (and (at Blank ?s2) (at ?t ?s1) (not (at Blank ?s1)) (not (at ?t ?s2)))
  )
)
