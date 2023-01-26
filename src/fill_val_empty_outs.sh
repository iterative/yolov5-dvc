val_dir="$1"
plots=("F1_curve.png" "P_curve.png" "PR_curve.png" "R_curve.png")

for plot in ${plots[@]}; do 
    if [ ! -f ${val_dir}/$plot ]; then 
        cp src/assets/no_data.png ${val_dir}/$plot
    fi;
done

if [ ! -f ${val_dir}/best_predictions.json ]; then 
    echo '{}' > ${val_dir}/best_predictions.json
fi;