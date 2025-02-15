import { Button } from "@/components/ui/button"

export type DateRange = 'all' | 'ytd' | 'q1' | 'q2' | 'q3' | 'q4'

interface DateFilterProps {
  value: DateRange
  onChange: (value: DateRange) => void
}

const DATE_OPTIONS = [
  { value: 'all', label: 'All Time' },
  { value: 'ytd', label: 'Year to Date' },
  { value: 'q1', label: 'Q1' },
  { value: 'q2', label: 'Q2' },
  { value: 'q3', label: 'Q3' },
  { value: 'q4', label: 'Q4' }
] as const

export default function DateFilter({ value = 'all', onChange }: DateFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {DATE_OPTIONS.map(({ value: optionValue, label }) => (
        <Button
          key={optionValue}
          variant={value === optionValue ? "default" : "outline"}
          size="sm"
          onClick={() => onChange(optionValue)}
        >
          {label}
        </Button>
      ))}
    </div>
  )
}