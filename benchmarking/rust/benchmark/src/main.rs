use std::{env};
use walkdir::WalkDir;


fn convert_bytes_to_string(all_bytes: &[u64;5]) -> (f64,&str){
    let units: [&str;5] = ["bytes","kilobytes","megabytes","gigabytes","terabytes"];
    let mut amount: f64 = 0.0;
    let mut unit: &str = "";

    for i in (0..units.len()).rev() {
        if all_bytes[i] == 0 {
            continue;
        }
        if amount == 0.0 {
        
            amount += all_bytes[i] as f64;
            unit = units[i];
            continue;
        }
        amount += all_bytes[i] as f64 /1000.0;
    }

    (amount,unit)

}

fn main() -> Result<(), std::io::Error> {
    let mut all_bytes: [u64; 5] = [0, 0, 0, 0, 0];
    let args: Vec<String> = env::args().collect();
    let mut bench_mark_folder = "./benchmarking/benchmarkfolders";
    let mut file_amount: i32 = 0;
    if args.len() == 1 {
        println!("Benchmarking on ./benchmarking/benchmarkfolders")
    } else {
        bench_mark_folder = &args[1];
    }
    for entry in WalkDir::new( bench_mark_folder)
        .into_iter()
        .filter_map(Result::ok)
        .filter(|e| !e.file_type().is_dir())
    {
        file_amount += 1;
        all_bytes[0] += entry.metadata()?.len();
        let mut idx: usize = 0;
        while idx < all_bytes.len() {
            while all_bytes[idx] > 1000 {
                let transferred_bytes: u64 = all_bytes[idx] / 1000;
                all_bytes[idx + 1] += transferred_bytes;
                all_bytes[idx] -= transferred_bytes * 1000;
            }
            idx += 1;
        }
    }
    let (amount, unit) = convert_bytes_to_string(&all_bytes);
    println!("Total size of all folders: {} {} in {} files.",amount,unit,file_amount);
    Ok(())
}
