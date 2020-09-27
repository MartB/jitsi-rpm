#!/bin/bash

outdir=build
cur=$(pwd)
state=fail

for package in *; do
    if [[ -d "$package" ]] && [[ "$package" != "$outdir" ]]; then
        echo "Building $package"
        pushd $package > /dev/null
        mock --sources=. --spec=$package.spec --enable-network &> "$cur/$outdir/$package.log" && state=success
        if [[ "$state" = "success" ]]; then
           rpmlint /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm &> "$cur/$outdir/$package.lint"
           cp /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm $cur/$outdir
        fi
        echo "$package finished: $state"
        popd > /dev/null
    fi
done


#jitsi_meet=failed
#jicofo=failed
#jvb=failed
#jigasi=failed
#jibri=failed

#cd jitsi-meet
#mock --sources=. --spec=jitsi-meet.spec --enable-network && jitsi_meet=succeeded
#if [[ "$jitsi_meet" = "succeeded" ]]; then
#    rpmlint /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm > ../$build/jitsi-meet.lint
#    cp /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm ../packages || exit 1
#fi
#cd ..
#cd jicofo
#mock --sources=. --spec=jicofo.spec --enable-network && jicofo=succeeded
#if [[ "$jicofo" = "succeeded" ]]; then
#    rpmlint /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm > ../$build/jicofo.lint
#    cp /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm ../packages ||  exit 1
#fi
#cd ..
#cd jitsi-videobridge
#mock --sources=. --spec=jitsi-videobridge.spec --enable-network && jivb=succeeded
#if [[ "$jvb" = "succeeded" ]]; then
#    rpmlint /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm > ../$build/jvb.lint
#    cp /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm ../packages || exit 1
#fi
#cd ..
#cd jigasi
#mock --sources=. --spec=jigasi.spec --enable-network && jigasi=succeeded
#if [[ "$jigasi-meet" = "succeeded" ]]; then
#    rpmlint /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm > ../$build/jigasi.lint
#    cp /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm ../packages || exit 1
#fi
#cd ..
#cd jibri
#mock --sources=. --spec=jibri.spec --enable-network && jibri=succeeded
#if [[ "$jibri" = "succeeded" ]]; then
#    rpmlint /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm > ../$build/jibri.lint
#    cp /var/lib/mock/fedora-rawhide-x86_64/result/*.rpm ../packages || exit 1
#fi
#cd ..

#echo
#echo "Jitsi Meet: ${jits_-meet}"
#echo "Jicofo: ${jicofo}"
#echo "Jitsi-videobridge: ${jvb}"
#echo "Jigasi: ${jigasi}"
#echo "Jibri: ${jibri}"
