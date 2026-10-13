// car_world.fx
// The ONE small logic world that all ten pattern examples share.
// Every example loads this file unchanged and only adds the language model.

world closed.

// ---------------------------------------------------------------
// Schema: what a car is
// ---------------------------------------------------------------
Vehicle { wheels: Integer }.
Car extends Vehicle.
Car { hasSteeringWheel: Boolean }.

// ---------------------------------------------------------------
// Our three cars
// ---------------------------------------------------------------
golf:Car[wheels -> 4; hasSteeringWheel -> true; brakes -> ok].
beetle:Car[wheels -> 4; hasSteeringWheel -> true; brakes -> broken].
tesla:Car[wheels -> 4; hasSteeringWheel -> true].   // nobody has checked the brakes yet

// ---------------------------------------------------------------
// Can a car be driven?
// A car that is neither Drivable nor NotDrivable is a case
// the rules cannot decide (the tesla).
// ---------------------------------------------------------------
?C:Drivable    <- ?C:Car[wheels -> 4; hasSteeringWheel -> true; brakes -> ok].
?C:NotDrivable <- ?C:Car[brakes -> broken].

// ---------------------------------------------------------------
// Speed limits: a proposed speed is admitted only if it respects
// the limit of the zone.
// ---------------------------------------------------------------
schoolZone:Zone[limit -> 30].   // our local rule: 30 km/h near schools
highway:Zone[limit -> 120].
?P:Admitted <- ?P:Proposal[speed -> ?S; zone -> ?Z] AND ?Z[limit -> ?L] AND ?S <= ?L.

// ---------------------------------------------------------------
// Readings: a statement read from a text becomes a fact about a
// car only if its quote was found in that text.
// ---------------------------------------------------------------
?R:Accepted <- ?R:Reading[quoteFound -> true].
?C[?Slot -> ?Value] <- ?R:Accepted[car -> ?C; slot -> ?Slot; value -> ?Value].

// ---------------------------------------------------------------
// Pre-drive checklist: one check after the other.
// The next check is the first one that is not answered yet,
// and only if the check before it was answered with yes.
// ---------------------------------------------------------------
start[answer -> yes].
fuelCheck:Check[topic -> "enough fuel in the tank"; after -> start].
tyreCheck:Check[topic -> "enough air in the tyres"; after -> fuelCheck].
lightCheck:Check[topic -> "all lights working"; after -> tyreCheck].

?C:Answered <- ?C[answer -> ?A].
?C:Next     <- ?C:Check[after -> ?P] AND ?P[answer -> yes] AND NOT ?C:Answered.
?C:Failed   <- ?C:Check[answer -> no].
?C:Passed   <- ?C:Check[answer -> yes].

// ---------------------------------------------------------------
// Diagnosis: possible causes why a car does not start.
// A cause is ruled out if it contradicts what we can observe.
// ---------------------------------------------------------------
beetle[fuelGauge -> full; dashboardLights -> on].

?C:WontStart <- ?C[battery -> empty].
?C:WontStart <- ?C[fuel -> empty].
?C:WontStart <- ?C[starter -> broken].
?C:WontStart <- ?C[immobilizer -> active].

?C:Contradiction <- ?C[fuel -> empty; fuelGauge -> full].
?C:Contradiction <- ?C[battery -> empty; dashboardLights -> on].

// The question that decides whether a cause is really the one.
?C[askNext -> "Do you hear a click when you turn the key?"] <- ?C[starter -> broken].
?C[askNext -> "Does the key symbol blink on the dashboard?"] <- ?C[immobilizer -> active].
?C[askNext -> "Do the headlights get dim when you try to start?"] <- ?C[battery -> empty].
?C[askNext -> "When did you last fill the tank?"] <- ?C[fuel -> empty].

// ---------------------------------------------------------------
// Review: a remark about the rules counts as a finding for a person
// only if it quotes the policy text exactly.
// ---------------------------------------------------------------
?R:Finding <- ?R:Remark[quoteFound -> true].
