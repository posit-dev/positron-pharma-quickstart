# functions.R

# Entry point:
#   run_trial_analysis(trial_id = "PHARMA-101")

# Sets up the analysis for a clinical trial and calls generate_patient_data
# ------------------------------------------------------------------
run_trial_analysis <- function(trial_id, n_patients = 50) {
  cat("Starting analysis for trial:", trial_id, "\n")

  trial_name  <- paste("Clinical Trial", trial_id)
  start_date  <- Sys.Date()
  analyst     <- "Dr. Rivera"
  status      <- "in progress"

  results <- generate_patient_data(n_patients)
  results
}


# Simulates patient data and calls compute_statistics
# ------------------------------------------------------------------
generate_patient_data <- function(n) {
  set.seed(42)

  patient_ids <- paste0("PT-", sprintf("%03d", seq_len(n)))
  ages        <- sample(18:75, n, replace = TRUE)
  weights_kg  <- round(rnorm(n, mean = 75, sd = 15), 1)
  dosages_mg  <- round(weights_kg * 0.5, 2)
  sites       <- sample(c("Boston", "Chicago", "Houston"), n, replace = TRUE)

  patient_data <- data.frame(
    id      = patient_ids,
    age     = ages,
    weight  = weights_kg,
    dosage  = dosages_mg,
    site    = sites,
    stringsAsFactors = FALSE
  )

  compute_statistics(patient_data)
}


# Validates data and calls the final report function
# ------------------------------------------------------------------
compute_statistics <- function(data) {
  n_patients   <- nrow(data)
  mean_age     <- mean(data$age)
  mean_weight  <- mean(data$weight)
  dosage_range <- range(data$dosage)
  site_counts  <- table(data$site)

  required_columns <- c("id", "age", "weight", "dosage", "site", "response")
  missing_cols     <- setdiff(require_columns, names(data))

  if (length(missing_cols) > 0) {
    stop(
      paste(
        "Data validation failed. Missing required column(s):",
        paste(missing_cols, collapse = ", ")
      )
    )
  }

  format_results(data)
}

# Formats and prints the final report
# ------------------------------------------------------------------
format_results <- function(data) {
  report_title <- "=== Trial Analysis Report ==="
  n_sites      <- length(unique(data$site))
  avg_dosage   <- round(mean(data$dosage), 2)
  completion   <- paste0(nrow(data), " patients processed across ", n_sites, " sites.")

  cat(report_title, "\n")
  cat(completion, "\n")
  cat("Average dosage:", avg_dosage, "mg\n")

  invisible(list(
    n          = nrow(data),
    avg_dosage = avg_dosage,
    n_sites    = n_sites
  ))
}
