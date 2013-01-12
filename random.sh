#!/bin/bash

name=`sort -R distinct-names | head -1`
colour=`sort -R distinct-colours | head -1`
adjective=`sort -R distinct-adjectives | head -1`
animal=`sort -R distinct-animals | head -1`
verb=`sort -R distinct-verbs | head -1`
adverb=`sort -R distinct-adverbs | head -1`

echo "$name the $adjective $colour $animal $verb $adverb"
